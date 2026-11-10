# COLONIX – Design Handoff

Design source of truth for the Colony Counter web app (**COLONIX**).
Designer: **Mouad Bouchareb** · Project lead: Rahma · Repo: Lina

## Links
- Figma file: https://www.figma.com/design/BFPpFnLoaDfulug9p1Scq8/COLONIX-Design-System?node-id=0-1&t=SVCgXzRWQSaA9Ksj-1
- Interactive prototype: https://www.figma.com/proto/BFPpFnLoaDfulug9p1Scq8/COLONIX-Design-System?node-id=0-1&t=SVCgXzRWQSaA9Ksj-1
- Prototype start flow: **COLONIX Desktop · Start here**

> In Figma press `Shift + D` to open **Dev Mode** and inspect spacing, radius, colors and fonts.

## Folder structure
```
/design
  README.md                    ← this file
  tokens.md                    ← colors, fonts, spacing, radius
  tailwind.colors.snippet.js   ← Tailwind v3 theme
  colonix.theme.css            ← Tailwind v4 theme (@theme)
  /logo                        ← logo SVG + PNG
  /icons                       ← icon SVGs
  /screens                     ← PNG previews of each screen
```

## Quick start (React + Vite + Tailwind)
1. Install fonts: `npm i @fontsource/plus-jakarta-sans @fontsource/jetbrains-mono` (imports in `tokens.md`).
2. Add the theme:
   - Tailwind **v4** → import `design/colonix.theme.css` in your main CSS.
   - Tailwind **v3** → spread `colonixTheme` from `tailwind.colors.snippet.js` into `theme.extend`.
3. Use the tokens (`bg-bg-base`, `bg-panel`, `text-text-muted`, `text-accent-green`, `font-mono`…) instead of raw hex values.

## Design direction
Scientific / techy dark UI with teal and mint-green accents. The main focus is the circular
petri dish viewer with detected colonies marked as rings/dots, and a live count panel.
Numbers always use **JetBrains Mono**; everything else uses **Plus Jakarta Sans**.

## Brand palette
| Name | Hex |
|---|---|
| Slate Navy | `#394A6D` |
| Cadet Teal | `#3C9D9B` |
| Mint Emerald | `#52DE97` |
| Pale Mint | `#C0FFB3` |

Full UI color list (backgrounds, text, accents, opacities) is in [`tokens.md`](./tokens.md).

## Screens & states
| Screen / state | Notes |
|---|---|
| Desktop · Start here | Entry point of the prototype |
| Upload · Choose sample plate | Pick a demo plate or upload a photo |
| Uploaded sample plate | Plate preview before counting |
| Counting · Automatic completion | Count runs and finishes automatically |
| E. coli result | Sample count: 142 |
| S. aureus result | Sample count: 348 |
| B. subtilis result | Sample count: 24 |
| Magnified inspection (150%) | Zoom into the plate to check colonies |
| Reset manual adjustments | Restore the automatic count |
| Live camera demo | Camera-based counting demo |
| Export · Count report preview | Report preview before export |
| Mobile | Mobile layout |

> Counts shown (142 / 348 / 24) are **sample data** for the prototype.

## Layout specs
### Desktop (frame 1920 × 1081)
| Zone | Size (px) | Tailwind |
|---|---|---|
| Header | 1920 × 64 | `h-16 w-full` |
| Left panel | 340 × 1017 | `w-[340px]` |
| Center (plate viewer) | 1200 × 1017 | `flex-1` (fills remaining width) |
| Right panel | 380 × 1017 | `w-[380px]` |

340 + 1200 + 380 = 1920. Build it as a header on top and a 3-column row below it
(`flex h-[calc(100vh-4rem)]`). Side panels are fixed width; the center is flexible.

### Mobile (frame 388 × 845)
| Zone | Size (px) |
|---|---|
| Header | 388 × 52 |
| Main (plate viewer) | 388 × 554.5 |
| Mode switcher | 388 × 53 |
| Count sheet | 388 × 117.5 |
| Footer | 388 × 68 |

Heights add up to 845. Use full width (`w-full`) with fixed heights for the header, mode switcher,
count sheet and footer; the main area takes the remaining height (`flex-1`).
Fractional heights (554.5, 117.5) come from Figma, so rounding to whole pixels is fine.

## Main components
- Circular plate viewer (detection rings, zoom, overlay toggle)
- Count panel (total, manual adjustments: added / removed, net total)
- Species selector (E. coli, S. aureus, B. subtilis)
- Buttons (primary / secondary), upload card
- Report / export panel

## Behaviors to implement
- **Count display** = automatic count + net manual adjustments (add / remove colony).
- **Detection overlay** can be toggled ON / OFF.
- **Reset** restores the automatic count and clears manual adjustments (summary: "0 (0 added, 0 removed)").
- **Magnified inspection** zooms the plate up to 150%.

## Notes for devs
- The Figma **Variables** (`Colony 1 visible` … `Colony N visible`, `Count display`, `Overlay label`, …) exist **only to make the prototype interactive**. They are not design tokens; don't implement them.
- Spacing follows a 4 / 8 px scale (Tailwind default).
- Need an asset that's missing? Export it from Figma (SVG for logo and icons).
- Questions or changes → comment on the frame in Figma (`C`).
