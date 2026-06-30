# Paws & Prejudice

A raucous Regency TikTok soap opera where dogs are the middle class and cats are the aristocracy. 450 episodes, 15 seconds each. Pride and Prejudice retold as pure chaos.

## Project Structure

```
paws_and_prejudice/
├── assets/
│   ├── characters/     # 57 MJ character renders (PNG)
│   ├── locations/      # 35 MJ location renders (PNG)  
│   └── style/          # 2 style reference images
├── scripts/
│   ├── 15s/            # 15-second TikTok scripts
│   ├── 30s/            # 30-second expanded scripts
│   └── series_bible/   # Full series bible + loglines
├── renders/            # Rendered video output (.mp4)
├── thumbnails/
│   ├── logo/           # Brand logo + icon
│   └── episodes/       # Per-episode cover thumbnails
├── social/             # Captions, hashtags, copy
├── tools/              # Subtitle pipeline, utilities
└── README.md
```

## Characters (MJ Rendered)

**Core Cast:** Lady Woofington-Barks (Pomeranian), Lord Biscuit-Bottoms (Basset Hound), Eliza Fetchworth (Border Collie), Lord Darcy Pawsworth (Tuxedo Cat), Lord Bingley Fluffington (Ginger Tabby), Wickham (Siamese Cat), Caroline Bingley (Sphynx), Lady Catherine de Paw (White Persian), Mary Fetchworth (Dachshund), Lydia Fetchworth (Dalmatian), Kitty Fetchworth (Beagle), Jane Fetchworth (Golden Retriever), Mr Collins (Chihuahua), Charlotte Lucas (Labrador), Colonel Fitzwilliam (Springer Spaniel), Aunt Gardiner (Cocker Spaniel)

**Full Cast:** 54+ characters rendered. See `assets/characters/`.

## Rendering Pipeline

- **Model:** dreamina-seedance-2-0-mini-260615 (15s max)
- **Resolution:** 720p, 9:16 vertical
- **Cost:** $3.50/M tokens ($1.14 per 15s render)
- **Style:** PHOTOREALISTIC. 35mm film aesthetic, vintage period drama, subtle grain. NOT cartoon.
- **Audio:** Generated in-model with British voices + classical music + SFX
- **Watermark:** @pawsandprejudiceofficial (ffmpeg post-process)
- **Subtitles:** `tools/add_subs.sh` (Whisper + ffmpeg burn-in)

## Quick Start

```bash
# Render an episode
python3 render.py --ep 01 --script scripts/15s/SCRIPTS.md

# Add subtitles
./tools/add_subs.sh renders/EP01.mp4

# Add watermark
ffmpeg -i input.mp4 -vf "drawtext=text='@pawsandprejudiceofficial':fontfile=Georgia.ttf:fontsize=24:fontcolor=white@0.5:x=w-tw-20:y=h-th-20" output.mp4
```

## Missing Assets

6 character files on Dropbox could not be copied (resource lock):
- Lady Catherine de Paw, Mary Fetchworth, Sir Reginald Bumblechin III, The Archbishop of Snootington, The Honourable Gerald Wobblethwaite, Viscount Reginald Puddlesworth

These need manual copy from `/Users/davidsheldrick/Desktop/paws_refs/characters/`.
