# Paws & Prejudice — Hashtag Strategy
_Optimised for maximum reach and network effect across all platforms_

---

## Core Insight

Dogs + Cats = two massive audiences. Period drama = passionate niche. AI video = trending category.
The strategy: lead with animals (volume), layer in the niche (quality), add AI (discovery).

---

## TikTok — Primary Caption Format

**Max 5 hashtags** (algorithm rewards fewer, more targeted tags on TikTok)

**Tier 1 — Volume (pick 2):**
- #DogsOfTikTok (133M+ posts)
- #CatsOfTikTok (100M+ posts)
- #PetsOfTikTok (broad crossover)
- #FunnyPets
- #Fyp

**Tier 2 — Niche (pick 2):**
- #PawsAndPrejudice (own brand — build this up)
- #RegencyDogs
- #PrideAndPrejudice
- #CottageCore
- #PeridorDrama

**Tier 3 — Discovery (pick 1):**
- #AIVideo
- #AIAnimation
- #GenerativeAI
- #AIArt

**Recommended TikTok caption template:**
```
EP.{N}: {title} 🐾
#PawsAndPrejudice #DogsOfTikTok #CatsOfTikTok #PrideAndPrejudice #AIVideo
```

---

## Instagram — Full 30 Hashtag Set

Use all 30 in comments (not caption — keeps caption clean).

**Set A — Dog Episodes:**
```
#PawsAndPrejudice #DogsOfTikTok #DogsOfInstagram #DogsOfIG #DogLover #DogLife
#PuppiesOfInstagram #InstaDoc #DogOfTheDay #FunnyDogs #DogMom #PetLover
#CatsOfInstagram #CatsOfTikTok #CatLover #CatsAndDogs #PetsOfInstagram
#PrideAndPrejudice #Regency #RegencyEra #PeriodDrama #CottageCore #BridgertonVibes
#AIVideo #AIAnimation #AIArt #GenerativeAI #AIContent #ViralPets #Fyp
```

**Set B — Cat Episodes:**
```
#PawsAndPrejudice #CatsOfTikTok #CatsOfInstagram #CatLover #CatLife #FunnyCats
#KittiesOfInstagram #CatMom #PetsOfInstagram #InstaKitty #CatFeature
#DogsOfInstagram #DogsAndCats #PetLover #AnimalLovers #FunnyAnimals
#PrideAndPrejudice #Regency #RegencyEra #PeriodDrama #CottageCore
#AIVideo #AIAnimation #AIArt #GenerativeAI #AIContent #ViralAnimals #Fyp
#PawsAndPrejudice #RegencyDogs #RegencyCats
```

---

## YouTube Shorts — 3-5 Tags Only

YouTube Shorts treats hashtags differently — fewer is better, they appear as clickable chips.

```
#PawsAndPrejudice #DogsOfYouTube #AIVideo
```

For cat episodes add: `#CatsOfYouTube`
For dog episodes add: `#FunnyDogs`

**YouTube description template:**
```
EP.{N}: {title}

Paws & Prejudice — the AI micro-drama where dogs and cats navigate Regency England. 
450 episodes. 15 seconds each. All the drama, none of the manners.

🐾 New episodes daily.
Subscribe for the full series.

#PawsAndPrejudice #DogsOfYouTube #AIVideo #PrideAndPrejudice
```

---

## Chinese Platforms

### Douyin (抖音) — Chinese TikTok
Same content, Chinese hashtag overlay:
```
#宠物 #狗狗 #猫咪 #搞笑宠物 #AI视频 #英伦风 #PawsAndPrejudice
```
Translation: #pets #dogs #cats #funny pets #AI video #British style

### Xiaohongshu (小红书 / Little Red Book)
More lifestyle-focused, longer captions work:
```
#宠物 #狗狗日常 #猫咪 #英剧风 #AI创作 #PawsAndPrejudice #搞笑视频
```
Add English tags too — XHS has growing English-speaking audience.

### Bilibili (B站)
Video platform (like YouTube), tag system:
```
Tags: AI视频 宠物 搞笑 英伦 猫猫狗狗 AI动画
```

### Kuaishou (快手)
TikTok competitor in China, same approach as Douyin.

---

## Cross-Platform Posting Priority

| Platform | Audience Size | Setup Status | Priority |
|---|---|---|---|
| TikTok | 1B+ | ✅ Active | 1 |
| Instagram Reels | 2B+ | 🔄 Creating | 2 |
| YouTube Shorts | 2B+ | 🔄 Creating | 3 |
| Douyin | 700M+ | ⚠️ Phone verification needed | 4 |
| Xiaohongshu | 300M+ | ⚠️ Phone verification needed | 5 |
| Bilibili | 300M+ | ⚠️ Phone verification needed | 6 |
| Kuaishou | 600M+ | ⚠️ Phone verification needed | 7 |

---

## Network Effect Strategy

**The goal: build #PawsAndPrejudice as a brand hashtag.**

- Every post on every platform uses #PawsAndPrejudice
- Cross-promote: "Follow us on TikTok/IG/YouTube @pawsandprejudice"
- Build community: reply to comments in character (Lady W-B voice)
- Encourage duets/stitches/remixes on TikTok
- Post EP.001 pinned on all profiles as the series intro

**Timing:** Pet content peaks 6-9am, 12-2pm, 7-10pm local time.
Target posting: 09:00, 13:00, 18:00 (3x daily when ramping up).

---

## Auto-Posting Architecture (Monday)

```
Episodes folder → tiktok_batch_post.py
                → instagram_batch_post.py (to build)
                → youtube_batch_post.py (to build)
                → chinese_platforms.py (to build, needs VPN + phone)
```

Target: same video, platform-specific caption + hashtags, every hour.
