import asyncio
import logging
import os
import tempfile
from io import BytesIO
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from fastapi import FastAPI, File, Request, UploadFile
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from inference_sdk import InferenceConfiguration, InferenceHTTPClient
from inference_sdk.http.errors import (
    HTTPCallErrorError,
    HTTPClientError,
    HTTPServerConnectionError,
)
from PIL import Image, UnidentifiedImageError
from starlette.exceptions import HTTPException as StarletteHTTPException

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("colony-counter")

ROBOFLOW_API_URL = "https://serverless.roboflow.com"
DEFAULT_MODEL_ID = "bacteria-colonies-detection-wrka5/1"

ROBOFLOW_API_KEY = os.getenv("ROBOFLOW_API_KEY")
ROBOFLOW_MODEL_ID = os.getenv("ROBOFLOW_MODEL_ID", DEFAULT_MODEL_ID)
ALLOWED_ORIGINS = [
    origin.strip()
    for origin in os.getenv(
        "ALLOWED_ORIGINS",
        "http://localhost:5173,http://localhost:3000,http://127.0.0.1:5173",
    ).split(",")
    if origin.strip()
]
INFERENCE_TIMEOUT_SECONDS = float(os.getenv("INFERENCE_TIMEOUT_SECONDS", "60"))
MAX_UPLOAD_BYTES = 15 * 1024 * 1024

ALLOWED_SUFFIXES = {".jpg", ".jpeg", ".png"}
EXCLUDED_CLASS_MARKERS = ("defect", "contamination", "contaminant")

# The client is created once at startup and reused by every request.
roboflow_client: InferenceHTTPClient | None = None
if ROBOFLOW_API_KEY:
    roboflow_client = InferenceHTTPClient(
        api_url=ROBOFLOW_API_URL,
        api_key=ROBOFLOW_API_KEY,
    )
    # The legacy Roboflow route maps iou_threshold to "overlap".
    # Both thresholds are percentages (0-100), matching Roboflow's API.
    roboflow_client.configure(
        InferenceConfiguration(
            confidence_threshold=25,
            iou_threshold=30,
            api_key_transport="legacy",
        )
    )

app = FastAPI(title="Colony Counter API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


class APIError(Exception):
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message
        super().__init__(message)


@app.exception_handler(APIError)
async def api_error_handler(_request, exc: APIError) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"success": False, "error": exc.message},
    )


@app.exception_handler(RequestValidationError)
async def validation_error_handler(
    _request: Request, _exc: RequestValidationError
) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "error": "Invalid request. Upload an image using the 'file' field.",
        },
    )


@app.exception_handler(StarletteHTTPException)
async def http_error_handler(
    _request: Request, exc: StarletteHTTPException
) -> JSONResponse:
    message = exc.detail if isinstance(exc.detail, str) else "Request failed."
    return JSONResponse(
        status_code=exc.status_code,
        content={"success": False, "error": message},
    )


@app.exception_handler(Exception)
async def unexpected_error_handler(
    _request: Request, exc: Exception
) -> JSONResponse:
    logger.exception("Unexpected server error: %s", exc)
    return JSONResponse(
        status_code=500,
        content={"success": False, "error": "Unexpected server error."},
    )


def _is_colony(prediction: dict[str, Any]) -> bool:
    class_name = str(prediction.get("class", "")).lower()
    return not any(marker in class_name for marker in EXCLUDED_CLASS_MARKERS)


def _extract_predictions(result: Any) -> list[dict[str, Any]]:
    if isinstance(result, list):
        if not result:
            return []
        result = result[0]
    if not isinstance(result, dict):
        raise APIError(502, "Roboflow returned an unexpected response.")

    predictions = result.get("predictions", [])
    if isinstance(predictions, dict):
        predictions = predictions.get("predictions", [])
    if not isinstance(predictions, list):
        raise APIError(502, "Roboflow returned an unexpected predictions format.")
    return [p for p in predictions if isinstance(p, dict)]


@app.get("/api/health")
async def health() -> dict[str, Any]:
    configured = bool(ROBOFLOW_API_KEY and roboflow_client and ROBOFLOW_MODEL_ID)
    return {
        "status": "ok",
        "roboflow_configured": configured,
        "model_id": ROBOFLOW_MODEL_ID if configured else None,
    }


@app.post("/api/count")
async def count_colonies(file: UploadFile = File(...)) -> JSONResponse:
    if not ROBOFLOW_API_KEY or not roboflow_client or not ROBOFLOW_MODEL_ID:
        raise APIError(
            503,
            "Roboflow is not configured. Set ROBOFLOW_API_KEY and "
            "ROBOFLOW_MODEL_ID in the server environment.",
        )

    suffix = Path(file.filename or "").suffix.lower()
    if suffix not in ALLOWED_SUFFIXES:
        raise APIError(
            400, "Unsupported file type. Upload a JPG, JPEG or PNG image."
        )

    contents = await file.read()
    if not contents:
        raise APIError(400, "Uploaded file is empty.")
    if len(contents) > MAX_UPLOAD_BYTES:
        raise APIError(413, "Image is too large. Maximum size is 15 MB.")

    try:
        with Image.open(BytesIO(contents)) as image:
            image_format = image.format
            width, height = image.size
            image.verify()
    except (UnidentifiedImageError, OSError, ValueError, SyntaxError) as exc:
        raise APIError(400, "Uploaded file is not a valid image.") from exc

    if image_format not in {"JPEG", "PNG"}:
        raise APIError(400, "Only JPG, JPEG and PNG images are supported.")

    temp_path: str | None = None
    try:
        with tempfile.NamedTemporaryFile(
            delete=False, suffix=suffix, prefix="colony_"
        ) as temp_file:
            temp_file.write(contents)
            temp_path = temp_file.name

        try:
            result = await asyncio.wait_for(
                asyncio.to_thread(
                    roboflow_client.infer,
                    temp_path,
                    model_id=ROBOFLOW_MODEL_ID,
                ),
                timeout=INFERENCE_TIMEOUT_SECONDS,
            )
        except asyncio.TimeoutError as exc:
            raise APIError(
                504, "Roboflow inference timed out. Please try again."
            ) from exc
        except HTTPCallErrorError as exc:
            logger.error("Roboflow API error %s: %s", exc.status_code, exc.api_message)
            if exc.status_code in (401, 403):
                message = "Roboflow authentication failed. Check ROBOFLOW_API_KEY."
            elif exc.status_code == 404:
                message = (
                    f"Roboflow model '{ROBOFLOW_MODEL_ID}' was not found. "
                    "Check ROBOFLOW_MODEL_ID."
                )
            else:
                message = f"Roboflow inference failed: {exc.api_message or exc.description}"
            raise APIError(502, message) from exc
        except (HTTPServerConnectionError, HTTPClientError) as exc:
            logger.error("Roboflow client error: %s", exc)
            raise APIError(502, f"Could not reach Roboflow: {exc}") from exc
    finally:
        if temp_path:
            try:
                os.unlink(temp_path)
            except FileNotFoundError:
                pass
            except OSError:
                logger.warning("Could not delete temporary file %s", temp_path)

    predictions = _extract_predictions(result)
    colonies = []
    for prediction in predictions:
        if not _is_colony(prediction):
            continue
        try:
            colonies.append(
                {
                    "x": float(prediction["x"]),
                    "y": float(prediction["y"]),
                    "width": float(prediction["width"]),
                    "height": float(prediction["height"]),
                    "class": str(prediction.get("class", "unknown")),
                    "confidence": float(prediction.get("confidence", 0.0)),
                }
            )
        except (KeyError, TypeError, ValueError):
            logger.warning("Skipping malformed prediction: %s", prediction)

    return JSONResponse(
        content={
            "success": True,
            "total_colonies": len(colonies),
            "image_dimensions": {"width": width, "height": height},
            "colonies": colonies,
        }
    )
