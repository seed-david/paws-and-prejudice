# PAWS & PREJUDICE — Visual Styles

This project maintains **two parallel visual styles** for the same cast and world. Every subject can be rendered in either. Pick one per output; do not mix within a single frame. **One canonical ref per subject per style** — single source of truth.

---

## STYLE-1 — "Golden Vintage" (the original)

Lo-fi **vintage analog film photography**: real dogs in hand-made Regency costume, faded Kodachrome colour, dust, scratches, snapshot framing. Warm, kitsch, hand-crafted, funny.

- **Style plates:** `style-1/style_ref/` (golden vintage + golden regency)
- **Character refs:** `style-1/characters/` — **9 core characters**
- **Location refs:** `style-1/locations/` — Longbourn drawing room

| Ref file | Character | Breed |
|---|---|---|
| `eliza_ref.jpg` | Eliza Fetchworth | Border Collie |
| `darcy_ref.jpg` | Lord Darcy Pawsworth | Tuxedo cat |
| `bingley_ref.jpg` | Lord Bingley Fluffington | Ginger tabby |
| `mary_ref.jpg` | Mary Fetchworth | Dachshund |
| `wickham_ref.jpg` | Wickham | Siamese cat |
| `mr_collins_ref.jpg` | Mr Collins | Chihuahua |
| `colonel_fitzwilliam_ref.jpg` | Colonel Fitzwilliam | Springer Spaniel |
| `mr_bennet.jpg` | Lord Biscuit-Bottoms (the father) | Basset Hound |
| `mrs_bennet.jpg` | Lady Woofington-Barks (the mother) | Pomeranian |

Redundant `_v8` / `_compressed` version files were removed so each subject has exactly one canonical ref.

---

## STYLE-2 — "Premium Couture" (new)

Hyperreal, high-production **MidJourney / Seedream** renders: anthropomorphic dogs *and cats* in couture Regency dress, bipedal, on clean studio backdrops (characters) and opulent photoreal interiors/exteriors (locations). Cinematic, premium, brand-grade.

- **Manifest:** [`style-2/MANIFEST.md`](style-2/MANIFEST.md)
- **52 characters · 32 locations = 84 canonical refs** (one per subject).
- **Source:** `~/Documents/ComfyUI/output/PAWS&PREJUDICE_STYLE2/` (full alternate-take archive lives there, outside the repo).

Hero filenames follow the `RENDER_QUEUE.md` convention (e.g. `style-2/characters/LADY_WOOFINGTON-BARKS.png`), so `style-2/characters/` is a **drop-in ref set** for the Dreamina/Seedance render pipeline.

Style-2 covers the **full Series Bible roster** plus **13 brand-new characters** not yet written into the bible (Baron Drago von Knottenheim, Countess Valentina Meowkowski, Doña Esperanza del Fuego, Lady Ermengarde Floppsworth, Lord Percival Gobbleton, Madame Fifi la Plume, Sir Reginald Bumblechin III, The Archbishop of Snootington, The Honourable Gerald Wobblethwaite, Viscount Reginald Puddlesworth, Lt. Goodpaw, Professor Humphrey, Uncle Gardiner) — see MANIFEST.

**12 subjects folded in from the parallel render batch** during reconciliation: `DOG_FOOTMAN`, and 11 new interiors — Longbourn Breakfast Room / Library / Parlour / Sitting Room / Study, Meryton Milliner's Shop, Netherfield Ballroom / Breakfast Room / Drawing Room / Entrance Hall / Music Room.

---

## Storage

Style-2 PNGs are tracked with **Git LFS** (`.gitattributes`: `style-2/**/*.png`) to keep clones lean. After cloning: `git lfs install` then `git lfs pull`.

## Known gaps (for reconciliation)

- Style-1 only covers the 9 core characters; the remaining roster is style-2 only.
- `EXT. COUNTRY LANE – NIGHT` (Ep.1 script) has no premium style-2 render yet (a style-mismatched test plate exists outside the repo).
