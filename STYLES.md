# PAWS & PREJUDICE — Visual Styles

This project maintains **two parallel visual styles** for the same cast and world, now at **full parity** — every subject exists in both. One canonical ref per subject per style (single source of truth). Pick one style per output; do not mix within a frame.

| | Characters | Locations | Style plates |
|---|---|---|---|
| **style-1** (vintage) | 52 | 33 | 2 |
| **style-2** (premium) | 52 | 33 | — |

---

## STYLE-1 — "Golden Vintage"

Lo-fi **vintage analog film photography**: real dogs/cats in Regency costume, faded Kodachrome colour, soft focus, film grain, dust, scratches, light leaks. Warm, kitsch, hand-crafted.

- `style-1/characters/` — 52 (the 9 original photographic refs + the full roster restyled to vintage)
- `style-1/locations/` — 33
- `style-1/style_ref/` — golden vintage + golden regency plates
- Manifest: [`style-1/MANIFEST.md`](style-1/MANIFEST.md)

The 9 original refs keep their names (`eliza_ref.jpg`, `darcy_ref.jpg`, `mr_bennet.jpg` = Lord Biscuit-Bottoms, `mrs_bennet.jpg` = Lady Woofington-Barks, etc.); the rest use the canonical `RENDER_QUEUE` names. All new vintage renders are 4K JPG.

## STYLE-2 — "Premium Couture"

Hyperreal **MidJourney / Seedream** renders: anthropomorphic dogs *and cats* in couture Regency dress on clean studio backdrops (characters) and opulent photoreal interiors/exteriors (locations).

- `style-2/characters/` — 52 · `style-2/locations/` — 33
- Manifest: [`style-2/MANIFEST.md`](style-2/MANIFEST.md)
- Source / full take-archive: `~/Documents/ComfyUI/output/PAWS&PREJUDICE_STYLE2/`

Hero filenames follow the `RENDER_QUEUE.md` convention (e.g. `style-2/characters/LADY_WOOFINGTON-BARKS.png`) — a drop-in ref set for the render pipeline. Includes the full Series Bible roster **plus 13 new characters** not yet in the bible (Baron Drago von Knottenheim, Countess Valentina Meowkowski, Doña Esperanza del Fuego, Lady Ermengarde Floppsworth, Lord Percival Gobbleton, Madame Fifi la Plume, Sir Reginald Bumblechin III, The Archbishop of Snootington, The Honourable Gerald Wobblethwaite, Viscount Reginald Puddlesworth, Lt. Goodpaw, Professor Humphrey, Uncle Gardiner) — these still need bible entries.

---

## Gaps — all filled

- ✅ Full character roster now in **both** styles (was 9-only in style-1).
- ✅ Full location set now in **both** styles.
- ✅ `EXT. COUNTRY LANE – NIGHT` rendered in **both** styles (premium photoreal + vintage).

## Storage

Style-1 and style-2 raster refs are tracked with **Git LFS** (`.gitattributes`). After cloning: `git lfs install && git lfs pull`. Total LFS ≈ 0.57 GB.
