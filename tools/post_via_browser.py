#!/usr/bin/env python3
"""Paws & Prejudice — Browser Auto-Poster
Posts to TikTok, Instagram Reels, and YouTube Shorts via browser automation.
All platforms must be pre-logged-in via Chrome profile.

Usage:
  python3 tools/post_via_browser.py --ep 15 --platform youtube
  python3 tools/post_via_browser.py --ep 01-05 --platforms all
"""

import argparse, os, sys, time

DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RENDERS = os.path.join(DIR, "renders")

def get_video(ep_num):
    for f in sorted(os.listdir(RENDERS), reverse=True):
        if f.startswith(f"EP{ep_num:02d}") and f.endswith(".mp4") and not f.startswith("."):
            return os.path.join(RENDERS, f)
    return None

def get_caption(ep_num):
    return f"Paws & Prejudice — EP.{ep_num:02d}\n\n@pawsandprejudiceofficial\n\n#PawsAndPrejudice #RegencyDogTok #PeriodDrama #WebSeries #BritishComedy #DogTok #CatTok"

def post_youtube_browser(ep_num, video_path, caption):
    """Post to YouTube Shorts via browser (must be logged in to @pawsandprejudice YouTube channel)"""
    print(f"\n📤 YouTube Shorts — EP.{ep_num:02d}")
    print(f"   1. Navigate to: https://studio.youtube.com")
    print(f"   2. Click CREATE → Upload Shorts")
    print(f"   3. Upload: {video_path}")
    print(f"   4. Title: Paws & Prejudice EP.{ep_num:02d}")
    print(f"   5. Description: {caption[:100]}...")
    print(f"   6. Set to Public, check 'Made for Kids: No'")
    print(f"   7. Publish")
    
    # TODO: Full browser automation with OpenClaw browser tool
    # Steps:
    # 1. browser.navigate("https://studio.youtube.com")
    # 2. browser.act click CREATE button
    # 3. browser.act click "Upload Shorts"
    # 4. browser.upload file
    # 5. Fill title, description fields
    # 6. Click "Next" through to visibility
    # 7. Set Public, publish
    
    return "⚠️  Manual — needs credentials"

def post_tiktok_browser(ep_num, video_path, caption):
    """Post to TikTok via browser (must be logged in to @pawsandprejudice TikTok)"""
    print(f"\n📤 TikTok — EP.{ep_num:02d}")
    print(f"   1. Navigate to: https://www.tiktok.com/upload")
    print(f"   2. Upload: {video_path}")
    print(f"   3. Caption: {caption[:100]}...")
    print(f"   4. Post")
    return "⚠️  Manual — needs credentials"

def post_instagram_browser(ep_num, video_path, caption):
    """Post to Instagram Reels via browser (must be logged in to @pawsandprejudice Instagram)"""
    print(f"\n📤 Instagram — EP.{ep_num:02d}")
    print(f"   1. Navigate to: https://www.instagram.com/")
    print(f"   2. Click + → Reel")
    print(f"   3. Upload: {video_path}")
    print(f"   4. Caption: {caption[:100]}...")
    print(f"   5. Share")
    return "⚠️  Manual — needs credentials"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ep", required=True)
    parser.add_argument("--platforms", default="all")
    args = parser.parse_args()
    
    if "-" in args.ep:
        start, end = args.ep.split("-")
        episodes = list(range(int(start), int(end) + 1))
    else:
        episodes = [int(args.ep)]
    
    platforms = args.platforms.split(",") if args.platforms != "all" else ["youtube", "tiktok", "instagram"]
    
    print(f"🚀 Paws & Prejudice Auto-Poster")
    print(f"   Episodes: {episodes}")
    print(f"   Platforms: {', '.join(platforms)}")
    print(f"   {'-'*40}")
    
    for ep in episodes:
        video = get_video(ep)
        if not video:
            print(f"❌ EP.{ep:02d}: No rendered video found")
            continue
        
        caption = get_caption(ep)
        print(f"\n📺 EP.{ep:02d} — {os.path.basename(video)}")
        
        if "youtube" in platforms:
            print(post_youtube_browser(ep, video, caption))
        if "tiktok" in platforms:
            print(post_tiktok_browser(ep, video, caption))
        if "instagram" in platforms:
            print(post_instagram_browser(ep, video, caption))

if __name__ == "__main__":
    main()
