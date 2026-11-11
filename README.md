# Colony Counter Project

Building a web app that counts bacterial colonies in a petri dish photo.

## Repository Contents

- `design/` — COLONIX UI/UX design handoff, design tokens, logo, icons, and screen previews. See [`design/README.md`](design/README.md).
- `backend/` — FastAPI backend that sends uploaded plate images to Roboflow hosted inference and returns colony counts.

## Backend

A minimal FastAPI backend for counting bacterial colonies using Roboflow hosted inference.

### Features

- Upload a JPG, JPEG, or PNG image and receive colony detections.
- Validates file type, image contents, and image dimensions with Pillow.
- Excludes non-colony classes such as `Defect`, `Contamination`, and `Contaminant`.
- Returns real Roboflow predictions with coordinates, size, class, and confidence.
- Handles missing configuration, API errors, and timeouts with consistent JSON errors.
- Deletes temporary image files even when inference fails.
- CORS restricted to configurable frontend origins.

### Tech Stack

- Python 3.11–3.13
- FastAPI
- Uvicorn
- [inference-sdk](https://inference.roboflow.com/) (Roboflow hosted inference)
- Pillow
- python-multipart
- python-dotenv

> Python 3.14 is not supported by the pinned `inference-sdk` version. Use Python 3.11, 3.12, or 3.13.

### Setup

```powershell
cd backend

py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1

pip install -r requirements.txt

Copy-Item .env.example .env
```

On macOS/Linux:

```bash
cd backend
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Edit `backend/.env` and set your Roboflow **Private API Key**:

```dotenv
ROBOFLOW_API_KEY=your_private_roboflow_key
ROBOFLOW_MODEL_ID=bacteria-colonies-detection-wrka5/1
ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000
INFERENCE_TIMEOUT_SECONDS=60
```

The API key must have access to the selected model. The model is used through Roboflow's hosted API; nothing is trained or downloaded locally.

### Run

```powershell
cd backend
.\.venv\Scripts\python.exe -m uvicorn main:app --host 127.0.0.1 --port 8000
```

Interactive API docs: <http://127.0.0.1:8000/docs>

### API

#### `GET /api/health`

Returns whether the API is running and whether Roboflow is configured.

```json
{
  "status": "ok",
  "roboflow_configured": true,
  "model_id": "bacteria-colonies-detection-wrka5/1"
}
```

`roboflow_configured` only checks that credentials are present. It does not validate the key until `/api/count` is called.

#### `POST /api/count`

Accepts a multipart form upload with a `file` field.

```powershell
curl.exe -X POST -F "file=@C:\path\to\plate.jpg" http://127.0.0.1:8000/api/count
```

Example success response:

```json
{
  "success": true,
  "total_colonies": 2,
  "image_dimensions": {
    "width": 640,
    "height": 640
  },
  "colonies": [
    {
      "x": 120.0,
      "y": 150.0,
      "width": 30.0,
      "height": 30.0,
      "class": "B-subtilis",
      "confidence": 0.94
    },
    {
      "x": 300.0,
      "y": 210.0,
      "width": 28.0,
      "height": 28.0,
      "class": "B-subtilis",
      "confidence": 0.89
    }
  ]
}
```

Error response:

```json
{
  "success": false,
  "error": "Uploaded file is not a valid image."
}
```

### Detection Settings

The Roboflow client is created once at startup and configured with:

- `confidence = 25`
- `overlap = 30`

These values are percentages, matching Roboflow's API.

### Limits

- Accepted formats: JPG, JPEG, PNG
- Maximum upload size: 15 MB
- Request timeout: configurable with `INFERENCE_TIMEOUT_SECONDS` (default 60 seconds)

### Notes for Deployment

This backend is suitable for a small university project or MVP. Before exposing it publicly:

- Add authentication or rate limiting so only your frontend can consume Roboflow credits.
- Serve it behind HTTPS and a reverse proxy.
- Keep `ROBOFLOW_API_KEY` server-side; never put it in frontend code.
- Use a process manager or container and restrict CORS to your deployed frontend origin.
- Add automated tests if the project is graded on testing.

The API deliberately returns errors instead of fake predictions when credentials or the model are unavailable.

## Design

The COLONIX design handoff includes the Figma source, tokens, Tailwind themes, logo, icons, and desktop/mobile screen previews. Start with [`design/README.md`](design/README.md).
