#!/usr/bin/env python3
# Paws & Prejudice — Auto-Poster
# Posts rendered episodes to TikTok, Instagram Reels, and YouTube Shorts
#
# Usage:
#   python3 tools/auto_post.py --ep 15 --platforms tiktok,youtube,instagram
#   python3 tools/auto_post.py --ep 01-05 --platforms all
#
# Requirements per platform:
#   YouTube: OAuth client_secret.json (run once to auth)
#   TikTok:  Browser session (login via Chrome)
#   Instagram: Browser session (login via Chrome)

import argparse, os, sys, subprocess, json, time

DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RENDERS = os.path.join(DIR, "renders")
SOCIAL = os.path.join(DIR, "social")

def get_video(ep_num):
    """Find rendered video for episode"""
    ep_str = f"EP{ep_num:02d}"
    for f in os.listdir(RENDERS):
        if f.startswith(ep_str) and f.endswith(".mp4"):
            return os.path.join(RENDERS, f)
    return None

def get_caption(ep_num):
    """Get social copy for episode"""
    # TODO: Load from social/ directory
    caption_file = os.path.join(SOCIAL, f"EP{ep_num:02d}_copy.md")
    if os.path.exists(caption_file):
        with open(caption_file) as f:
            return f.read()
    return f"Paws & Prejudice EP.{ep_num:02d} — new episode now live. @pawsandprejudiceofficial"

def get_thumbnail(ep_num):
    """Get thumbnail for episode"""
    thumb_dir = os.path.join(DIR, "thumbnails", "episodes")
    for f in os.listdir(thumb_dir):
        if f.startswith(f"EP{ep_num:02d}") and f.endswith(".png"):
            return os.path.join(thumb_dir, f)
    return None

def post_youtube(video_path, caption, thumbnail_path, ep_num):
    """Post to YouTube Shorts using YouTube Data API"""
    # Requires: pip install google-auth google-auth-oauthlib google-api-python-client
    try:
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
        from googleapiclient.discovery import build
        from googleapiclient.http import MediaFileUpload
    except ImportError:
        print("⚠️  YouTube API packages not installed. Run: pip install google-auth google-auth-oauthlib google-api-python-client")
        return False
    
    SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
    CLIENT_SECRETS = os.path.join(DIR, "tools", "youtube_client_secret.json")
    TOKEN_FILE = os.path.join(DIR, "tools", "youtube_token.json")
    
    if not os.path.exists(CLIENT_SECRETS):
        print("❌ YouTube: Missing client_secret.json in tools/")
        print("   Get it from: https://console.cloud.google.com/apis/credentials")
        return False
    
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS, SCOPES)
        creds = flow.run_local_server(port=8080)
        with open(TOKEN_FILE, "w") as f:
            f.write(creds.to_json())
    
    youtube = build("youtube", "v3", credentials=creds)
    
    title = f"Paws & Prejudice EP.{ep_num:02d} #shorts"
    description = caption + "\n\n#PawsAndPrejudice #RegencyDogTok #Shorts"
    
    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": ["PawsAndPrejudice", "RegencyDogTok", "shorts", "period drama", "comedy"],
            "categoryId": "22"  # People & Blogs
        },
        "status": {
            "privacyStatus": "public",
            "selfDeclaredMadeForKids": False
        }
    }
    
    media = MediaFileUpload(video_path, mimetype="video/mp4", resumable=True)
    request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)
    
    print(f"📤 YouTube: Uploading EP.{ep_num:02d}...")
    response = request.execute()
    print(f"✅ YouTube: https://youtube.com/shorts/{response['id']}")
    return True

def post_tiktok(video_path, caption, ep_num):
    """Post to TikTok via browser automation (OpenClaw browser tool)"""
    print(f"📤 TikTok: EP.{ep_num:02d} requires browser automation")
    print("   → Open https://www.tiktok.com/upload in Chrome")
    print("   → Upload: {video_path}")
    print("   → Caption: {caption[:100]}...")
    print("   ⚠️  TikTok requires manual posting via browser for now.")
    print("   To automate: provide TikTok session cookies or use scheduling tool.")
    return False

def post_instagram(video_path, caption, thumbnail_path, ep_num):
    """Post to Instagram Reels via browser automation"""
    print(f"📤 Instagram: EP.{ep_num:02d} requires browser automation")
    print("   → Open https://www.instagram.com/ in Chrome")
    print("   → Create Reel → Upload: {video_path}")
    print("   → Caption: {caption[:100]}...")
    print("   ⚠️  Instagram requires manual posting or Meta Graph API setup.")
    return False

def main():
    parser = argparse.ArgumentParser(description="Paws & Prejudice Auto-Poster")
    parser.add_argument("--ep", required=True, help="Episode number (e.g., 15 or 01-05)")
    parser.add_argument("--platforms", default="all", help="tiktok,youtube,instagram or all")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be posted")
    args = parser.parse_args()
    
    # Parse episode range
    if "-" in args.ep:
        start, end = args.ep.split("-")
        episodes = list(range(int(start), int(end) + 1))
    else:
        episodes = [int(args.ep)]
    
    platforms = args.platforms.split(",") if args.platforms != "all" else ["youtube", "tiktok", "instagram"]
    
    for ep in episodes:
        video = get_video(ep)
        if not video:
            print(f"❌ EP.{ep:02d}: No rendered video found in renders/")
            continue
        
        caption = get_caption(ep)
        thumbnail = get_thumbnail(ep)
        
        print(f"\n📺 EP.{ep:02d} — {os.path.basename(video)}")
        
        if args.dry_run:
            print(f"   [DRY RUN] Caption: {caption[:80]}...")
            continue
        
        results = {}
        if "youtube" in platforms:
            results["youtube"] = post_youtube(video, caption, thumbnail, ep)
        if "tiktok" in platforms:
            results["tiktok"] = post_tiktok(video, caption, ep)
        if "instagram" in platforms:
            results["instagram"] = post_instagram(video, caption, thumbnail, ep)
        
        print(f"   Results: {', '.join(f'{k}={\"✅\" if v else \"⚠️\"}' for k, v in results.items())}")

if __name__ == "__main__":
    main()
