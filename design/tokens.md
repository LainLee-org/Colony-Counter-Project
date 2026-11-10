# COLONIX – Design Tokens

## 1. Brand palette (official)
| Token | Name | Hex | Closest CSS name | Usage |
|---|---|---|---|---|
| `colonix-navy` | Slate Navy | `#394A6D` | darkslategray | Brand base, headers, dark surfaces |
| `colonix-teal` | Cadet Teal | `#3C9D9B` | cadetblue | Secondary brand color, buttons, active states |
| `colonix-emerald` | Mint Emerald | `#52DE97` | mediumaquamarine | Highlights, colony detections, success |
| `colonix-mint` | Pale Mint | `#C0FFB3` | palegreen | Light accents, soft highlights |

## 2. UI colors (as used in the Figma screens)
Extracted from the fills in the design file.

### Backgrounds & surfaces
| Token | Hex | Usage |
|---|---|---|
| `bg-base` | `#1C2638` | App background |
| `panel` | `#25334A` | Cards / side panels |
| `panel-raised` | `#2C3C56` | Raised / hovered panels |
| `border` | `#364968` | Borders, dividers, inactive controls |
| `border-subtle` | `#334155` | Subtle lines |
| `green-deep` | `#022C22` | Dark green tint / text on bright green |

### Text
| Token | Hex | Usage |
|---|---|---|
| `text` | `#F1F5F9` | Main text |
| `text-soft` | `#E2E8F0` | Secondary headings |
| `text-muted` | `#94A3B8` | Labels, captions |
| `text-faint` | `#CBD5E1` | Light-gray text |
| `blue-gray` | `#7E9BB8` | Muted blue-gray accents |
| `gray-400` / `gray-300` | `#9CA3AF` / `#D1D5DB` | Neutral grays |

### Accents & states
| Token | Hex | Usage |
|---|---|---|
| `accent-teal` | `#339989` | Primary action, active, rings (opacity 15–70% for tints) |
| `accent-green` | `#4CE08A` | Detections, success, live count |
| `accent-mint` | `#B8F9A6` | Soft highlight |
| `warning` | `#FBBF24` | Warnings / manual-adjustment states |

> ⚠️ **Heads-up:** the UI fills are very close to, but not identical to, the brand palette
> (e.g. `#339989` vs `#3C9D9B`, `#4CE08A` vs `#52DE97`, `#B8F9A6` vs `#C0FFB3`, `#364968` vs `#394A6D`).
> Devs should implement the **UI colors** (what the screens show) and use the brand palette for
> the logo, marketing and README. If the team prefers one set, update the Figma styles first.

Opacity variants of teal (`#339989` at 15, 20, 25, 30, 40, 50, 60, 70%), of `#1C2638` (40–95%) and of
`#25334A` (80–95%) are used for overlays, glass panels and glows.

## 3. Typography
| Role | Font | Weights |
|---|---|---|
| Headings / UI text | **Plus Jakarta Sans** | SemiBold (600), ExtraBold (800) |
| Numbers (counts, stats) | **JetBrains Mono** | Regular (400), Medium (500), Bold (700, big numbers) |

| Style | Font | Weight | Size / Line height |
|---|---|---|---|
| H1 | Plus Jakarta Sans | ExtraBold | `TODO` |
| H2 | Plus Jakarta Sans | SemiBold | `TODO` |
| Body / labels | Plus Jakarta Sans | SemiBold | `TODO` |
| Caption | Plus Jakarta Sans | SemiBold | `TODO` |
| Count number (big) | JetBrains Mono | Bold | `TODO` |
| Small numbers / stats | JetBrains Mono | Regular / Medium | `TODO` |

Install (Vite + React):
```bash
npm i @fontsource/plus-jakarta-sans @fontsource/jetbrains-mono
```
```js
// main.jsx
import '@fontsource/plus-jakarta-sans/600.css';
import '@fontsource/plus-jakarta-sans/800.css';
import '@fontsource/jetbrains-mono/400.css';
import '@fontsource/jetbrains-mono/500.css';
import '@fontsource/jetbrains-mono/700.css';
```

## 4. Spacing
4, 8, 12, 16, 24, 32, 48 px (Tailwind: 1, 2, 3, 4, 6, 8, 12)

## 5. Radius
| Element | Radius |
|---|---|
| Buttons | `TODO px` |
| Inputs | `TODO px` |
| Cards / panels | `TODO px` |
| Plate viewer | `full` (circle) |

## 6. Shadows / effects
`TODO` (glow on detections, panel blur, if used)
