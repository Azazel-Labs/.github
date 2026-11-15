# Profile art

The SVGs here are generated, and text is converted to outlines so they render the same everywhere with no web fonts.

| File | What it is |
|---|---|
| `banner-dark.svg`, `banner-light.svg` | Animated header: a garden grows, a weed sprouts, and the logo goat (`src/goat.py`) trots in and eats it |
| `stages-dark.svg`, `stages-light.svg` | Plant → Tend → Weed → Harvest strip |
| `card-twokey.svg`, `card-ferreal.svg`, `card-samplyd.svg` | 2:1 cards for projects that don't have hero art yet |
| `divider.svg` | Row of swaying sprouts between sections |

Every other picture on the profile comes straight from each project's own README art, so it stays current on its own.

## Regenerating

```sh
pip install uharfbuzz
mkdir -p src/fonts src/out
# Fraunces (roman + italic) and JetBrains Mono variable fonts, from github.com/google/fonts (OFL)
curl -L -o src/fonts/Fraunces.ttf        "https://raw.githubusercontent.com/google/fonts/main/ofl/fraunces/Fraunces%5BSOFT,WONK,opsz,wght%5D.ttf"
curl -L -o src/fonts/Fraunces-Italic.ttf "https://raw.githubusercontent.com/google/fonts/main/ofl/fraunces/Fraunces-Italic%5BSOFT,WONK,opsz,wght%5D.ttf"
curl -L -o src/fonts/JetBrainsMono.ttf   "https://raw.githubusercontent.com/google/fonts/main/ofl/jetbrainsmono/JetBrainsMono%5Bwght%5D.ttf"
cd src && python banner.py && python stages.py && python cards.py && python divider.py
cp out/*.svg ..
```

All the animations respect `prefers-reduced-motion`.
