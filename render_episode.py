#!/usr/bin/env python3
"""
PAWS & PREJUDICE — Automated Render + Thumbnail Pipeline
Usage: python3 render_episode.py <EP_NUMBER> <TITLE> <PROMPT_FILE> [--refs IMG1 IMG2...]

Reads prompt from file, submits video render, generates thumbnail,
logs everything to SPENDING_TRACKER.csv.
"""

import subprocess, json, base64, os, sys, time, csv
from datetime import datetime

KEY = "ark-950f075f-2019-4984-8680-326e4938ae6c-c11b5"
VIDEO_API = "https://ark.ap-southeast.bytepluses.com/api/v3/contents/generations/tasks"
IMAGE_API = "https://ark.ap-southeast.bytepluses.com/api/v3/images/generations"
DIR = "/Users/davidsheldrick/Desktop/paws_and_prejudice"
THUMB_DIR = f"{DIR}/thumbnails"
TRACKER = f"{DIR}/SPENDING_TRACKER.csv"

# Pricing
VIDEO_RATE = 3.50       # USD/M tokens (dreamina-seedance-2-0-mini, 720p, no video input)
THUMB_COST = 0.035      # USD/image (seedream-5-0-lite)
VIDEO_MODEL = "dreamina-seedance-2-0-mini-260615"
THUMB_MODEL = "seedream-5-0-lite-260128"

os.makedirs(THUMB_DIR, exist_ok=True)

def b64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def img_url(path):
    ext = path.split(".")[-1].lower()
    mime = "image/jpeg" if ext in ("jpg", "jpeg") else "image/png"
    return f"data:{mime};base64,{b64(path)}"

def submit_video(ep, title, prompt_text, refs):
    """Submit video generation, return task ID."""
    content = [{"type": "text", "text": prompt_text}]
    for ref in refs:
        content.append({"type": "image_url", "image_url": {"url": img_url(ref)}, "role": "reference_image"})
    
    payload = {
        "model": VIDEO_MODEL,
        "content": content,
        "generate_audio": True,
        "ratio": "9:16",
        "duration": 15,
        "watermark": False
    }
    
    result = subprocess.run([
        "curl", "-s", "-w", "\nHTTP:%{http_code}", VIDEO_API,
        "-H", "Content-Type: application/json",
        "-H", f"Authorization: Bearer {KEY}",
        "-d", json.dumps(payload),
    ], capture_output=True, text=True, timeout=60)
    
    body = result.stdout.split("\nHTTP:")[0]
    data = json.loads(body)
    if "id" not in data:
        raise Exception(f"Video submission failed: {body[:200]}")
    return data["id"]

def poll_video(task_id, timeout_minutes=10):
    """Poll until complete, return (video_url, tokens, resolution)."""
    url = f"{VIDEO_API}/{task_id}"
    for i in range(timeout_minutes * 6):
        time.sleep(10)
        result = subprocess.run(["curl", "-s", url, "-H", f"Authorization: Bearer {KEY}"],
                              capture_output=True, text=True, timeout=15)
        data = json.loads(result.stdout)
        status = data.get("status", "?")
        if status == "succeeded":
            return (data["content"]["video_url"],
                    data["usage"]["total_tokens"],
                    data.get("resolution", "?"))
        elif status in ("failed", "error"):
            raise Exception(f"Video failed: {json.dumps(data, indent=2)[:300]}")
    raise TimeoutError(f"Video {task_id} timed out after {timeout_minutes}min")

def generate_thumbnail(ep, title):
    """Generate episode thumbnail using Seedream 5 Lite."""
    prompt = f"""TikTok thumbnail cover image, Regency period drama comedy. A dramatic scene from the episode titled '{title}' featuring anthropomorphic dogs and cats in Regency clothing. Rich warm sepia tones, Bridgerton lighting, golden candlelight. Center composition with clear focal point. Upper third slightly darker for text overlay. Cinematic quality, warm and inviting. Animal magnetism — cute anthropomorphic animals in period costumes being dramatic and funny."""
    
    payload = {
        "model": THUMB_MODEL,
        "prompt": prompt,
        "size": "1920x1920",
        "n": 1,
        "response_format": "url",
        "watermark": False
    }
    
    result = subprocess.run([
        "curl", "-s", "-w", "\nHTTP:%{http_code}", IMAGE_API,
        "-H", "Content-Type: application/json",
        "-H", f"Authorization: Bearer {KEY}",
        "-d", json.dumps(payload),
    ], capture_output=True, text=True, timeout=60)
    
    body = result.stdout.split("\nHTTP:")[0]
    data = json.loads(body)
    if "data" not in data or len(data["data"]) == 0:
        raise Exception(f"Thumbnail generation failed: {body[:200]}")
    return data["data"][0]["url"]

def log_spending(ep, version, duration, resolution, tokens, video_cost, has_thumb, notes=""):
    """Append to spending tracker CSV."""
    thumb_cost = THUMB_COST if has_thumb else 0
    total = video_cost + thumb_cost
    today = datetime.now().strftime("%Y-%m-%d")
    
    with open(TRACKER, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([today, ep, version, duration, resolution, tokens,
                        f"{video_cost:.2f}", f"{thumb_cost:.3f}", f"{total:.2f}",
                        "✅", notes])

# ---- MAIN ----
if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python3 render_episode.py EP_NUMBER TITLE PROMPT_FILE [--refs IMG...]")
        sys.exit(1)
    
    ep = sys.argv[1]
    title = sys.argv[2]
    prompt_file = sys.argv[3]
    
    # Parse refs
    refs = []
    if "--refs" in sys.argv:
        idx = sys.argv.index("--refs")
        refs = sys.argv[idx+1:]
    
    with open(prompt_file) as f:
        prompt = f.read()
    
    print(f"🎬 Rendering {ep}: '{title}'")
    print(f"   Prompt: {len(prompt)} chars, {len(refs)} ref images")
    
    # 1. Submit video
    task_id = submit_video(ep, title, prompt, refs)
    print(f"   Video task: {task_id}")
    
    # 2. Generate thumbnail in parallel
    print(f"   Generating thumbnail...")
    try:
        thumb_url = generate_thumbnail(ep, title)
        thumb_file = f"{THUMB_DIR}/thumb_{ep.lower()}.png"
        subprocess.run(["curl", "-s", "-L", "-o", thumb_file, thumb_url], capture_output=True, timeout=30)
        thumb_ok = os.path.exists(thumb_file) and os.path.getsize(thumb_file) > 1000
        print(f"   Thumbnail: {'✅' if thumb_ok else '❌'} {os.path.getsize(thumb_file)/1024:.0f}KB")
    except Exception as e:
        print(f"   Thumbnail failed: {e}")
        thumb_ok = False
    
    # 3. Poll video
    print(f"   Polling...")
    video_url, tokens, resolution = poll_video(task_id)
    video_cost = (tokens / 1_000_000) * VIDEO_RATE
    
    # 4. Download video
    video_file = f"{DIR}/{ep}_{title.replace(' ', '_')}.mp4"
    subprocess.run(["curl", "-s", "-L", "-o", video_file, video_url], capture_output=True, timeout=120)
    video_size = os.path.getsize(video_file)
    
    # 5. Log
    log_spending(ep, "auto", "15s", resolution, tokens, video_cost, thumb_ok, title)
    
    print(f"\n✅ COMPLETE: {ep}")
    print(f"   Video: {video_file} ({resolution}, {video_size/1024/1024:.1f}MB)")
    print(f"   Tokens: {tokens:,} → ${video_cost:.2f} USD")
    print(f"   Thumbnail: {'${:.3f}'.format(THUMB_COST) if thumb_ok else 'FAILED'}")
    print(f"   Total: ${video_cost + (THUMB_COST if thumb_ok else 0):.2f} USD")
