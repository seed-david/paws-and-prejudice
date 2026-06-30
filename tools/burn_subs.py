#!/usr/bin/env python3
"""Paws & Prejudice — Subtitle Burner
Burns perfect script-accurate subtitles using ffmpeg drawtext (no SRT file issues).

Usage:
  python3 tools/burn_subs.py renders/EP01_v3_CHARACTER.mp4 --ep 01
"""

import subprocess, os, sys, argparse

SCRIPTS = {
    "01": [
        ("BISCUIT. CAT. NETHERFIELD. RICH.", 0.0, 4.48),
        ("Mm.", 8.30, 8.88),
        ("FIVE DAUGHTERS.", 10.38, 11.28),
        ("He has not turned a page in 12 years.", 12.06, 14.54),
    ],
    "02": [
        ("There. Ten thousand a year.", 0.5, 3.0),
        ("Insufferable dogs.", 3.5, 5.5),
        ("He's perfect.", 6.0, 7.5),
        ("She will marry this man to one of them.", 8.5, 12.0),
    ],
    "03": [
        ("Bonnet fought a hedge.", 0.5, 2.5),
        ("I heard that.", 3.0, 4.5),
        ("Good.", 5.0, 5.5),
        ("It will take them 6 episodes to admit this is flirting.", 7.0, 11.5),
    ],
    "04": [
        ("Collins the Chihuahua gets the house when you die.", 0.5, 3.5),
        ("I'm fine.", 4.0, 5.0),
        ("WE WILL LIVE IN A HEDGE.", 5.5, 8.0),
        ("He is very much not fine.", 9.0, 11.5),
    ],
    "05": [
        ("Bingley left. Caroline wrote this.", 0.5, 3.0),
        ("Says Jane isn't pretty enough.", 3.5, 6.0),
        ("Nobody ever recovers from the first bad letter.", 7.0, 10.5),
    ],
}

STYLE = "fontcolor=white:fontsize=40:box=1:boxcolor=black@0.6:boxborderw=12:x=(w-text_w)/2:y=h-th-140:line_spacing=10"

MAX_CHARS_PER_LINE = 28

def wrap_text(text, max_chars=MAX_CHARS_PER_LINE):
    """Wrap text to multiple lines, splitting at word boundaries"""
    words = text.split()
    lines = []
    current = ""
    for word in words:
        test = f"{current} {word}".strip()
        if len(test) <= max_chars:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return "\\n".join(lines) if len(lines) > 1 else text

def build_filters(lines):
    filters = []
    for text, start, end in lines:
        wrapped = wrap_text(text)
        escaped = wrapped.replace("'", "\\'").replace(":", "\\:")
        f = f"drawtext=text='{escaped}':{STYLE}:enable='between(t,{start},{end})'"
        filters.append(f)
    return ",".join(filters)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("video")
    parser.add_argument("--ep", required=True)
    parser.add_argument("--output", default=None)
    args = parser.parse_args()
    
    if args.ep not in SCRIPTS:
        print(f"❌ EP.{args.ep} not in subtitle database. Add it to tools/burn_subs.py")
        sys.exit(1)
    
    lines = SCRIPTS[args.ep]
    filters = build_filters(lines)
    
    if not args.output:
        base = os.path.splitext(args.video)[0]
        args.output = f"{base}_subtitled.mp4"
    
    print(f"🎬 EP.{args.ep}: {len(lines)} subtitle lines → {args.output}")
    
    cmd = [
        "ffmpeg", "-y", "-loglevel", "error",
        "-i", args.video,
        "-vf", filters,
        "-c:a", "copy",
        args.output
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ {result.stderr[:200]}")
        sys.exit(1)
    
    sz = os.path.getsize(args.output)
    print(f"✅ {sz/1024/1024:.1f}MB")

if __name__ == "__main__":
    main()
