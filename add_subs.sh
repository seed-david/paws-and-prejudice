#!/bin/bash
# Paws & Prejudice Subtitle Pipeline
# Usage: ./add_subs.sh input.mp4 [output.mp4]
# Auto-transcribes audio with Whisper, burns subtitles with ffmpeg

INPUT="$1"
OUTPUT="${2:-${INPUT%.mp4}_subtitled.mp4}"
BASENAME="$(basename "$INPUT" .mp4)"
TMPDIR="/tmp/pnp_subs_$$"

mkdir -p "$TMPDIR"

echo "🎙️ Extracting audio..."
ffmpeg -y -loglevel error -i "$INPUT" -vn -ar 16000 -ac 1 "$TMPDIR/audio.wav"

echo "📝 Transcribing with Whisper..."
whisper "$TMPDIR/audio.wav" --model tiny --language en --output_dir "$TMPDIR" --output_format srt 2>/dev/null

SRT_FILE=$(ls "$TMPDIR"/*.srt 2>/dev/null | head -1)
if [ -z "$SRT_FILE" ]; then
    echo "❌ No SRT generated"
    rm -rf "$TMPDIR"
    exit 1
fi

echo "🎬 Burning subtitles..."
ffmpeg -y -loglevel error \
    -i "$INPUT" \
    -vf "subtitles=$SRT_FILE:force_style='FontName=Georgia,FontSize=18,PrimaryColour=&HFFFFFF,OutlineColour=&H000000,Outline=2,Shadow=1,MarginV=40,Alignment=2'" \
    -c:a copy \
    "$OUTPUT"

SIZE=$(ls -la "$OUTPUT" | awk '{print $5}')
echo "✅ Done: $OUTPUT ($(echo "scale=1; $SIZE/1048576" | bc)MB)"

rm -rf "$TMPDIR"
