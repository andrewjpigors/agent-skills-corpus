---
name: ai-reels-pipeline
description: Orchestrate the AI Reels production pipeline — generate HeyGen avatars, curate B-roll assets, plan storyboards with Claude, generate Veo AI clips, assemble JSON configs, and render split-screen Instagram Reels via Remotion. Use when the user mentions "reels", "reel pipeline", "instagram reel", "avatar video", "storyboard", "veo clips", "render reel", or wants to produce short-form video content.
argument-hint: "<command> [options] — e.g. 'new my-reel --script \"text\"', 'curate my-reel', 'storyboard my-reel', 'full my-reel'"
user-invocable: true
---

# AI Reels Pipeline - Build Automated Instagram Reels with Claude Code

A complete, open-source pipeline for producing professional Instagram Reels using AI avatars, AI-generated B-roll, and automated video rendering - all orchestrated through Claude Code.

**What it does:** You write a script, the pipeline generates an AI avatar speaking it, finds/creates B-roll footage, plans a visual storyboard using Claude, assembles everything into a JSON config, and renders a polished split-screen reel via Remotion - with quality gates at every step.

**Stack:** Python + TypeScript/React (Remotion) + Claude API + HeyGen API + Google Veo API + FFmpeg + Whisper

---

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Prerequisites](#prerequisites)
3. [Project Setup](#project-setup)
4. [Directory Structure](#directory-structure)
5. [Pipeline Flow](#pipeline-flow)
6. [Stage 0: Pre-Pipeline (Script + Avatar + Transcribe)](#stage-0-pre-pipeline)
7. [Stage 1: Asset Curator](#stage-1-asset-curator)
8. [Stage 2: Storyboard Agent](#stage-2-storyboard-agent)
9. [Stage 2.5: Image Resolver](#stage-25-image-resolver)
10. [Stage 3: Veo Agent (AI Video Generation)](#stage-3-veo-agent)
11. [Stage 4: Assembly](#stage-4-assembly)
12. [Stage 5: Review](#stage-5-review)
13. [Remotion Rendering System](#remotion-rendering-system)
14. [JSON Config Schema (ReelConfig)](#json-config-schema)
15. [All Source Code](#all-source-code)
16. [Claude Code Integration](#claude-code-integration)
17. [Design Principles](#design-principles)
18. [Troubleshooting](#troubleshooting)

---

## Architecture Overview

```
1080x1920 (9:16 portrait, 25fps)
+--------------------------+
|                          |
|    TOP HALF (960px)      |  B-roll: video clips, screenshots, AI-generated
|    JSON-driven segments  |  Ken Burns zoom, crossfade transitions
|                          |
+--[purple pill caption]---+  Word-by-word caption at the seam
|                          |
|   BOTTOM HALF (960px)    |  AI avatar video (HeyGen)
|   Cropped + centered     |  Audio source for the entire reel
|                          |
+--------------------------+
```

### Pipeline Flow

```
Script -> HeyGen Avatar -> Speed Up (1.1x) -> Whisper Transcribe ->
  Asset Curator [GATE] -> Storyboard [GATE] -> Image Resolver -> Veo (on-demand) ->
  Assembly -> Render -> Review [GATE]
       ^                                                              |
       +------ fix loop (max 3 iterations) --------------------------+
```

Every reel is driven by a single JSON config file. No new React code per reel - just data.

---

## Prerequisites

### Required Software

```bash
# Node.js (for Remotion)
node --version  # v18+ required

# Python 3.10+
python3 --version

# FFmpeg (for video processing + quality analysis)
brew install ffmpeg  # macOS
# or: sudo apt install ffmpeg  # Linux

# Whisper (for transcription) - choose one:
pip install mlx-whisper  # Apple Silicon (recommended, fast)
# or:
pip install openai-whisper  # Cross-platform (requires PyTorch)
```

### API Keys

You'll need accounts and API keys for:

| Service | Purpose | Env Variable | Pricing |
|---------|---------|-------------|---------|
| [HeyGen](https://heygen.com) | AI avatar video generation | `HEYGEN_API_KEY` | ~$24/mo Creator plan |
| [Anthropic](https://console.anthropic.com) | Claude API for storyboard planning | `ANTHROPIC_API_KEY` | Pay per token |
| [Google AI Studio](https://aistudio.google.com) | Veo 3.1 AI video generation | `GOOGLE_API_KEY` | ~$0.60-1.60/clip |

Create a `.env` file in your project root:

```bash
HEYGEN_API_KEY=your_heygen_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
GOOGLE_API_KEY=your_google_api_key_here
```

---

## Project Setup

```bash
# 1. Create project directory
mkdir ai-reels-pipeline && cd ai-reels-pipeline

# 2. Initialize Node.js project (for Remotion)
npm init -y
npm install remotion@4.0.428 @remotion/cli@4.0.428 @remotion/media@4.0.428 \
  @remotion/google-fonts@4.0.428 @remotion/transitions@4.0.428 \
  typescript@5.9.3 @types/react @types/react-dom

# 3. Create Python virtual environment
python3 -m venv .venv
source .venv/bin/activate
pip install anthropic requests mlx-whisper  # or openai-whisper instead of mlx-whisper
pip install google-genai  # For Veo AI video generation

# 4. Create the directory structure (see below)
# 5. Copy all source files from this guide into place
```

### tsconfig.json

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "commonjs",
    "jsx": "react-jsx",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "outDir": "./dist",
    "rootDir": "./src"
  },
  "include": ["src/**/*"]
}
```

---

## Directory Structure

```
ai-reels-pipeline/
├── .env                           # API keys (gitignored)
├── package.json                   # Remotion + dependencies
├── tsconfig.json
│
├── src/                           # Remotion compositions (TypeScript/React)
│   ├── Root.tsx                   # Composition registry
│   ├── DynamicReel.tsx            # PRIMARY: JSON-driven reel composition
│   ├── components/
│   │   ├── DynamicBRoll.tsx       # B-roll renderer (video + images)
│   │   ├── DynamicCaptionOverlay.tsx  # Word-by-word purple pill captions
│   │   └── DynamicSceneRenderer.tsx   # Scene template router (optional overlays)
│   ├── scenes/templates/          # 8 parameterized scene types
│   │   ├── HookTemplate.tsx
│   │   ├── BulletsTemplate.tsx
│   │   ├── FeatureGridTemplate.tsx
│   │   ├── BigNumberTemplate.tsx
│   │   ├── ContrastTemplate.tsx
│   │   ├── StrikethroughTemplate.tsx
│   │   ├── LogoGridTemplate.tsx
│   │   └── ClosingTemplate.tsx
│   └── lib/
│       ├── constants.ts           # FPS, dimensions, colors, typography
│       └── dynamic-config.ts      # TypeScript interfaces for JSON config
│
├── public/                        # Static assets (served by Remotion)
│   ├── config/                    # JSON reel configs
│   │   └── reel-config-*.json
│   ├── avatars/                   # HeyGen avatar videos (sped up 1.1x)
│   ├── broll/
│   │   ├── clips/                 # Video clips (Veo AI + screen recordings)
│   │   └── topics/                # Per-topic image assets
│   ├── logos/                     # Brand logos for overlays
│   └── sfx/                      # Sound effects (optional)
│
├── heygen/                        # Avatar generation
│   ├── heygen_client.py           # HeyGen API wrapper
│   ├── generate.py                # CLI: generate avatar video
│   ├── transcribe.py              # Whisper transcription
│   ├── heygen_config.json         # Avatar/voice profiles
│   └── output/                    # Generated avatars + transcripts
│
├── ai-video-exploration/          # Veo AI video generation
│   ├── generate_broll.py          # Shot list -> Veo API -> MP4 clips
│   ├── config.json                # Gemini API key
│   ├── shot-lists/                # Per-reel shot list JSONs
│   └── outputs/                   # Generated clips
│
├── pipeline/                      # Python automation pipeline
│   ├── agents/
│   │   ├── pipeline_state.py      # State tracking across stages
│   │   ├── asset_curator.py       # Stage 1: collect + grade footage
│   │   ├── storyboard.py          # Stage 2: Claude plans visual timeline
│   │   ├── image_resolver.py      # Stage 2.5: Wikipedia image downloader
│   │   ├── veo_agent.py           # Stage 3: Veo AI clip generation
│   │   ├── assembly.py            # Stage 4: build ReelConfig JSON
│   │   ├── reviewer.py            # Stage 5: post-render QA
│   │   ├── __init__.py
│   │   └── output/                # Per-reel state directories
│   └── __init__.py
│
├── out/                           # Rendered output videos
└── raw-footage/                   # Source footage for B-roll
```

---

## Pipeline Flow

### Quick Start (End-to-End)

```bash
# 1. Write your script (max ~100 words for 45s reel)
SCRIPT="Claude Code just changed everything. It lives inside your terminal and understands your entire codebase. Edit files. Run tests. Create pull requests. Developers are shipping 10x faster. This isn't a copilot, it's an autonomous coding agent."

# 2. Generate HeyGen avatar
cd heygen
python3 generate.py --profile my-avatar --script "$SCRIPT"
# Output: output/<task-id>.mp4

# 3. Speed up 1.1x (more energetic feel)
ffmpeg -i output/<task-id>.mp4 \
  -filter_complex "[0:v]setpts=PTS/1.1[v];[0:a]atempo=1.1[a]" \
  -map "[v]" -map "[a]" -c:v libx264 -preset fast -crf 18 -c:a aac -b:a 192k \
  ../public/avatars/avatar-my-reel.mp4

# 4. Transcribe the sped-up version (timestamps will be correct)
python3 transcribe.py ../public/avatars/avatar-my-reel.mp4
# Output: ../public/avatars/avatar-my-reel_transcript.json

# 5. Initialize pipeline
cd ../pipeline
python3 -m agents.pipeline_state my-reel-v1 --init \
  --tool "My Product" \
  --transcript "../public/avatars/avatar-my-reel_transcript.json" \
  --avatar "avatars/avatar-my-reel.mp4" \
  --script "$SCRIPT"

# 6. Run each stage (see detailed sections below)
python3 -m agents.asset_curator --reel-id my-reel-v1 --tool "My Product"
python3 -m agents.storyboard --reel-id my-reel-v1
python3 -m agents.image_resolver --reel-id my-reel-v1
python3 -m agents.veo_agent --reel-id my-reel-v1
python3 -m agents.assembly --reel-id my-reel-v1 --render
python3 -m agents.reviewer --reel-id my-reel-v1
```

---

## Stage 0: Pre-Pipeline

Before the automated pipeline begins, you need three things:
1. A script (max ~100 words for a 45s reel)
2. An AI avatar video of someone speaking the script
3. A word-level transcript with timestamps

### HeyGen Config

Create `heygen/heygen_config.json`:

```json
{
  "api_key": "YOUR_HEYGEN_API_KEY",
  "avatars": {
    "my_avatar": "YOUR_AVATAR_ID"
  },
  "voices": {
    "my_voice": "YOUR_VOICE_ID"
  },
  "profiles": {
    "default": {
      "avatar_id": "YOUR_AVATAR_ID",
      "avatar_name": "My Avatar",
      "voice_id": "YOUR_VOICE_ID",
      "voice_name": "My Voice",
      "voice_emotion": "Excited",
      "voice_speed": 1.0,
      "notes": "Primary avatar profile"
    }
  }
}
```

### HeyGen Client (`heygen/heygen_client.py`)

```python
"""HeyGen API client wrapper. Handles auth, video generation, polling, and download."""

import requests
import time
import json
import os

API_BASE = "https://api.heygen.com"
UPLOAD_BASE = "https://upload.heygen.com"
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "heygen_config.json")


def load_api_key():
    if not os.path.exists(CONFIG_PATH):
        raise FileNotFoundError(f"Missing {CONFIG_PATH}")
    with open(CONFIG_PATH) as f:
        config = json.load(f)
    key = config.get("api_key", "")
    if not key or key == "YOUR_HEYGEN_API_KEY":
        raise ValueError("Set your real HeyGen API key in heygen_config.json")
    return key


def load_config():
    with open(CONFIG_PATH) as f:
        return json.load(f)


def get_profile(profile_name):
    config = load_config()
    profiles = config.get("profiles", {})
    if profile_name not in profiles:
        available = ", ".join(profiles.keys()) or "(none)"
        raise ValueError(f"Unknown profile '{profile_name}'. Available: {available}")
    return profiles[profile_name]


def headers(api_key=None):
    key = api_key or load_api_key()
    return {
        "X-Api-Key": key,
        "Content-Type": "application/json",
        "Accept": "application/json",
    }


def list_avatars(api_key=None):
    resp = requests.get(f"{API_BASE}/v2/avatars", headers=headers(api_key))
    resp.raise_for_status()
    return resp.json()


def list_voices(api_key=None):
    resp = requests.get(f"{API_BASE}/v2/voices", headers=headers(api_key))
    resp.raise_for_status()
    return resp.json()


def generate_video(
    script, avatar_id, voice_id, title="Test Video",
    dimension=None, background=None, avatar_style="normal",
    voice_speed=1.0, voice_emotion=None, callback_url=None, api_key=None,
):
    if dimension is None:
        dimension = {"width": 1080, "height": 1920}
    if background is None:
        background = {"type": "color", "value": "#000000"}

    voice_config = {
        "type": "text",
        "voice_id": voice_id,
        "input_text": script,
        "speed": voice_speed,
    }
    if voice_emotion:
        voice_config["emotion"] = voice_emotion

    payload = {
        "video_inputs": [{
            "character": {
                "type": "avatar",
                "avatar_id": avatar_id,
                "avatar_style": avatar_style,
            },
            "voice": voice_config,
            "background": background,
        }],
        "dimension": dimension,
        "title": title,
    }
    if callback_url:
        payload["callback_url"] = callback_url

    resp = requests.post(f"{API_BASE}/v2/video/generate", headers=headers(api_key), json=payload)
    resp.raise_for_status()
    data = resp.json()
    if data.get("error"):
        raise RuntimeError(f"HeyGen error: {data['error']}")

    video_id = data["data"]["video_id"]
    print(f"Video generation started: {video_id}")
    return video_id


def check_status(video_id, api_key=None):
    resp = requests.get(
        f"{API_BASE}/v1/video_status.get",
        params={"video_id": video_id},
        headers=headers(api_key),
    )
    resp.raise_for_status()
    return resp.json()["data"]


def wait_for_video(video_id, poll_interval=15, timeout=600, api_key=None):
    start = time.time()
    last_status = None
    while time.time() - start < timeout:
        data = check_status(video_id, api_key)
        status = data.get("status")
        if status != last_status:
            elapsed = int(time.time() - start)
            print(f"  [{elapsed}s] Status: {status}")
            last_status = status
        if status == "completed":
            print(f"  Video ready! Duration: {data.get('duration', '?')}s")
            return data
        if status == "failed":
            raise RuntimeError(f"Video generation failed: {data.get('error', 'unknown')}")
        time.sleep(poll_interval)
    raise TimeoutError(f"Video not ready after {timeout}s")


def download_video(video_url, output_path):
    print(f"  Downloading to {output_path}...")
    resp = requests.get(video_url, stream=True)
    resp.raise_for_status()
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    with open(output_path, "wb") as f:
        for chunk in resp.iter_content(chunk_size=8192):
            f.write(chunk)
    size_mb = os.path.getsize(output_path) / (1024 * 1024)
    print(f"  Downloaded: {size_mb:.1f} MB")
    return output_path
```

### Avatar Generator (`heygen/generate.py`)

```python
#!/usr/bin/env python3
"""Generate a HeyGen avatar video. End-to-end: submit -> poll -> download."""

import argparse
import json
import os
import sys

from heygen_client import generate_video, wait_for_video, download_video, get_profile

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")


def main():
    parser = argparse.ArgumentParser(description="Generate a HeyGen avatar video")
    parser.add_argument("--profile", help="Named profile from heygen_config.json")
    parser.add_argument("--avatar", help="Avatar ID (overrides profile)")
    parser.add_argument("--voice", help="Voice ID (overrides profile)")
    parser.add_argument("--script", required=True, help="Script text")
    parser.add_argument("--title", default="Reel Video", help="Video title")
    parser.add_argument("--landscape", action="store_true", help="16:9 instead of 9:16")
    parser.add_argument("--timeout", type=int, default=600, help="Max wait seconds")
    args = parser.parse_args()

    avatar_id = args.avatar
    voice_id = args.voice
    voice_speed = 1.0
    voice_emotion = None

    if args.profile:
        profile = get_profile(args.profile)
        avatar_id = avatar_id or profile["avatar_id"]
        voice_id = voice_id or profile["voice_id"]
        voice_speed = profile.get("voice_speed", 1.0)
        voice_emotion = profile.get("voice_emotion")

    if not avatar_id or not voice_id:
        print("Error: provide --profile or both --avatar and --voice")
        sys.exit(1)

    dimension = (
        {"width": 1920, "height": 1080} if args.landscape
        else {"width": 1080, "height": 1920}
    )

    print(f"\nGenerating video...")
    video_id = generate_video(
        script=args.script, avatar_id=avatar_id, voice_id=voice_id,
        title=args.title, dimension=dimension,
        voice_speed=voice_speed, voice_emotion=voice_emotion,
    )

    print(f"\nWaiting for video {video_id}...")
    result = wait_for_video(video_id, poll_interval=15, timeout=args.timeout)

    video_url = result["video_url"]
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_path = os.path.join(OUTPUT_DIR, f"{video_id}.mp4")
    download_video(video_url, output_path)

    meta_path = os.path.join(OUTPUT_DIR, f"{video_id}_meta.json")
    with open(meta_path, "w") as f:
        json.dump(result, f, indent=2)

    print(f"\nDone! Video: {output_path}")
    print(f"Duration: {result.get('duration', '?')}s")


if __name__ == "__main__":
    main()
```

### Transcriber (`heygen/transcribe.py`)

```python
#!/usr/bin/env python3
"""Transcribe a video using Whisper with word-level timestamps."""

import argparse
import json
import os
import sys

try:
    import mlx_whisper
    _USE_MLX = True
except ImportError:
    import whisper
    _USE_MLX = False


def transcribe(video_path: str, model_name: str = "base") -> dict:
    if _USE_MLX:
        repo = f"mlx-community/whisper-{model_name}"
        print(f"Transcribing with mlx_whisper ({repo}): {video_path}")
        result = mlx_whisper.transcribe(video_path, path_or_hf_repo=repo, word_timestamps=True)
    else:
        print(f"Loading Whisper model '{model_name}'...")
        model = whisper.load_model(model_name)
        print(f"Transcribing: {video_path}")
        result = model.transcribe(video_path, word_timestamps=True)

    words = []
    for segment in result["segments"]:
        for w in segment.get("words", []):
            words.append({
                "word": w["word"].strip(),
                "start": round(w["start"], 3),
                "end": round(w["end"], 3),
            })

    segments = []
    for seg in result["segments"]:
        segments.append({
            "text": seg["text"].strip(),
            "start": round(seg["start"], 3),
            "end": round(seg["end"], 3),
        })

    return {"text": result["text"].strip(), "words": words, "segments": segments}


def main():
    parser = argparse.ArgumentParser(description="Transcribe video with word timestamps")
    parser.add_argument("video", help="Path to video file")
    parser.add_argument("--model", default="base", help="Whisper model size")
    parser.add_argument("--output", "-o", help="Output JSON path")
    args = parser.parse_args()

    if not os.path.exists(args.video):
        print(f"Error: {args.video} not found")
        sys.exit(1)

    transcript = transcribe(args.video, args.model)

    output_path = args.output or f"{os.path.splitext(args.video)[0]}_transcript.json"
    with open(output_path, "w") as f:
        json.dump(transcript, f, indent=2)

    print(f"\nTranscript saved: {output_path}")
    print(f"  Words: {len(transcript['words'])}")


if __name__ == "__main__":
    main()
```

---

## Stage 1: Asset Curator

Scans your asset library, grades each file on visual quality (brightness, resolution, motion), and outputs an approved/rejected manifest.

**Quality scoring:**
- Brightness (0-255): FFmpeg signalstats YAVG. Reject < 30, warn < 50
- Resolution: Reject below 720p minimum dimension
- Duration (video): Reject below 3 seconds
- Motion score (video): FFmpeg scene detection, 0-100
- Overall quality score: Composite 0-100. Reject < 40

**CLI:**
```bash
python3 -m pipeline.agents.asset_curator \
  --reel-id my-reel-v1 \
  --tool "My Product" \
  [--youtube "product demo tutorial"] \
  [--extra-dir /path/to/screen-recordings] \
  [--scan-all]
```

**Output:** `pipeline/agents/output/<reel-id>/asset-manifest.json`

**Gate:** Review which assets were approved/rejected before proceeding.

### Source: `pipeline/agents/asset_curator.py`

```python
"""Asset Curator Agent: collect, scan, and grade all raw B-roll footage."""

import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

PIPELINE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_DIR = os.path.dirname(PIPELINE_DIR)
BROLL_DIR = os.path.join(PROJECT_DIR, "public", "broll")
CLIPS_DIR = os.path.join(BROLL_DIR, "clips")
TOPICS_DIR = os.path.join(BROLL_DIR, "topics")
LOGOS_DIR = os.path.join(PROJECT_DIR, "public", "logos")

# Quality thresholds
BRIGHTNESS_REJECT = 30
BRIGHTNESS_WARN = 50
QUALITY_REJECT = 40
MIN_RESOLUTION = 720
MIN_VIDEO_DURATION = 3.0

IMAGE_EXTS = (".png", ".jpg", ".jpeg", ".webp")
VIDEO_EXTS = (".mp4", ".webm", ".mov")


def _ffprobe_info(filepath: str) -> dict:
    try:
        cmd = ["ffprobe", "-v", "quiet", "-print_format", "json",
               "-show_streams", "-show_format", filepath]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
        if result.returncode != 0:
            return {}
        return json.loads(result.stdout)
    except (subprocess.TimeoutExpired, json.JSONDecodeError, FileNotFoundError):
        return {}


def _get_brightness(filepath: str, is_video: bool = False) -> float:
    try:
        input_args = ["-i", filepath]
        if is_video:
            input_args = ["-t", "3"] + input_args

        cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error",
               *input_args, "-vf", "signalstats", "-f", "null", "-"]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

        yavg_values = []
        for line in result.stderr.split("\n"):
            if "YAVG" in line:
                parts = line.split("YAVG=")
                if len(parts) > 1:
                    try:
                        yavg_values.append(float(parts[1].split()[0]))
                    except (ValueError, IndexError):
                        pass
        if yavg_values:
            return sum(yavg_values) / len(yavg_values)
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    return -1


def _get_motion_score(filepath: str) -> float:
    try:
        cmd = ["ffmpeg", "-hide_banner", "-loglevel", "info",
               "-t", "5", "-i", filepath,
               "-vf", "select='gt(scene,0.1)',metadata=print", "-f", "null", "-"]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        scene_changes = result.stderr.count("scene_score=")
        return min(scene_changes * 20, 100)
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return -1


def grade_asset(filepath: str) -> dict:
    is_video = filepath.lower().endswith(VIDEO_EXTS)
    result = {"brightness": -1, "resolution": "unknown", "width": 0, "height": 0}

    if is_video:
        result["duration_sec"] = 0.0
        result["motion_score"] = -1

    probe = _ffprobe_info(filepath)
    streams = probe.get("streams", [])
    video_stream = next((s for s in streams if s.get("codec_type") == "video"), None)
    if video_stream:
        w = int(video_stream.get("width", 0))
        h = int(video_stream.get("height", 0))
        result["width"] = w
        result["height"] = h
        result["resolution"] = f"{w}x{h}"

    if is_video:
        fmt = probe.get("format", {})
        duration = float(fmt.get("duration", 0))
        result["duration_sec"] = round(duration, 1)
        result["motion_score"] = _get_motion_score(filepath)

    result["brightness"] = round(_get_brightness(filepath, is_video=is_video), 1)

    # Compute overall quality score (0-100)
    score = 50
    brightness = result["brightness"]
    if brightness >= 0:
        if brightness >= 100: score += 30
        elif brightness >= BRIGHTNESS_WARN: score += 20
        elif brightness >= BRIGHTNESS_REJECT: score += 5
        else: score -= 25

    min_dim = min(result["width"], result["height"]) if result["width"] > 0 else 0
    if min_dim >= 1080: score += 20
    elif min_dim >= 720: score += 10
    elif min_dim > 0: score -= 10

    if is_video:
        dur = result["duration_sec"]
        if dur >= MIN_VIDEO_DURATION: score += 10
        elif dur > 0: score += 5
        motion = result.get("motion_score", -1)
        if motion >= 60: score += 10
        elif motion >= 30: score += 5

    result["quality_score"] = max(0, min(100, score))
    return result


def scan_and_grade(tool_name: str, scan_all: bool = False, extra_dirs: list = None) -> list:
    topic_key = tool_name.lower().replace(" ", "-")
    assets = []

    # Scan topic directory
    topic_dir = os.path.join(TOPICS_DIR, topic_key)
    if os.path.isdir(topic_dir):
        for f in sorted(os.listdir(topic_dir)):
            if f.lower().endswith(IMAGE_EXTS):
                filepath = os.path.join(topic_dir, f)
                grade = grade_asset(filepath)
                assets.append({
                    "id": os.path.splitext(f)[0], "type": "screenshot",
                    "path": f"topics/{topic_key}/{f}", "abs_path": filepath,
                    "source": "existing", **grade,
                })

    # Scan video clips
    if os.path.isdir(CLIPS_DIR):
        for f in sorted(os.listdir(CLIPS_DIR)):
            if not f.lower().endswith(VIDEO_EXTS): continue
            if scan_all or topic_key in f.lower():
                filepath = os.path.join(CLIPS_DIR, f)
                grade = grade_asset(filepath)
                assets.append({
                    "id": os.path.splitext(f)[0], "type": "video",
                    "path": f"clips/{f}", "abs_path": filepath,
                    "source": "existing", **grade,
                })

    # Scan extra directories
    for extra in (extra_dirs or []):
        if not os.path.isdir(extra): continue
        for f in sorted(os.listdir(extra)):
            if f.lower().endswith(IMAGE_EXTS + VIDEO_EXTS):
                filepath = os.path.join(extra, f)
                grade = grade_asset(filepath)
                is_video = f.lower().endswith(VIDEO_EXTS)
                assets.append({
                    "id": os.path.splitext(f)[0],
                    "type": "video" if is_video else "screenshot",
                    "path": f"clips/{f}", "abs_path": filepath,
                    "source": "screen_recording", **grade,
                })

    return assets


def apply_quality_gates(assets: list) -> list:
    for asset in assets:
        if asset.get("type") == "logo":
            asset["approved"] = True
            asset["rejection_reason"] = ""
            continue

        reasons = []
        brightness = asset.get("brightness", -1)
        if 0 <= brightness < BRIGHTNESS_REJECT:
            reasons.append(f"Too dark (brightness {brightness:.0f}/255)")

        min_dim = min(asset.get("width", 0), asset.get("height", 0))
        if 0 < min_dim < MIN_RESOLUTION:
            reasons.append(f"Resolution too low ({asset.get('resolution', '?')})")

        if asset.get("type") == "video":
            dur = asset.get("duration_sec", 0)
            if 0 < dur < MIN_VIDEO_DURATION:
                reasons.append(f"Too short ({dur:.1f}s)")

        score = asset.get("quality_score", 0)
        if score < QUALITY_REJECT and not reasons:
            reasons.append(f"Quality score too low ({score}/100)")

        asset["approved"] = len(reasons) == 0
        asset["rejection_reason"] = "; ".join(reasons) if reasons else ""
    return assets


def build_manifest(reel_id: str, tool_name: str, assets: list) -> dict:
    clean_assets = [{k: v for k, v in a.items() if k != "abs_path"} for a in assets]
    approved = [a for a in assets if a.get("approved")]
    rejected = [a for a in assets if not a.get("approved")]
    return {
        "reel_id": reel_id, "tool_name": tool_name,
        "curated_at": datetime.now(timezone.utc).isoformat(),
        "assets": clean_assets,
        "summary": {
            "total": len(assets), "approved": len(approved), "rejected": len(rejected),
        },
    }


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Asset Curator")
    parser.add_argument("--reel-id", required=True)
    parser.add_argument("--tool", required=True)
    parser.add_argument("--extra-dir", action="append", default=[])
    parser.add_argument("--scan-all", action="store_true")
    args = parser.parse_args()

    from pipeline.agents.pipeline_state import PipelineState
    state = PipelineState(args.reel_id)
    if not state.exists():
        state.init(tool_name=args.tool)

    print(f"  Curating assets for: {args.tool}")
    assets = scan_and_grade(args.tool, scan_all=args.scan_all, extra_dirs=args.extra_dir)
    if not assets:
        print(f"  No assets found. Add files to public/broll/topics/{args.tool.lower().replace(' ', '-')}/")
        return

    assets = apply_quality_gates(assets)
    manifest = build_manifest(args.reel_id, args.tool, assets)

    output_path = os.path.join(state.reel_dir, "asset-manifest.json")
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(manifest, f, indent=2)

    print(f"  Total: {manifest['summary']['total']} | Approved: {manifest['summary']['approved']}")
    state.complete_stage("curate", "asset-manifest.json", manifest["summary"])


if __name__ == "__main__":
    main()
```

---

## Stage 2: Storyboard Agent

Uses the Claude API to intelligently plan which visual appears at every moment of the reel, matching B-roll to speech content.

**Key rules:**
- 10-15 segments for a 30-45s reel
- 60%+ video clips (motion > static)
- Max 1-2 screenshots, never consecutive
- 2-3 Veo AI clips for visual variety
- Every B-roll must semantically match the speech
- Scene overlays disabled (they look cheap)

**CLI:**
```bash
python3 -m pipeline.agents.storyboard \
  --reel-id my-reel-v1 \
  [--model claude-sonnet-4-20250514]
```

**Output:** `pipeline/agents/output/<reel-id>/storyboard.json`

### Source: `pipeline/agents/storyboard.py`

The full storyboard agent is ~650 lines. The key components are:

1. **System prompt** - Detailed instructions for Claude on visual grammar, pacing, banned types, and semantic matching rules
2. **User prompt builder** - Feeds transcript, approved assets, and constraints to Claude
3. **Response parser** - Extracts the storyboard JSON and validates segment contiguity

See the [full source in the All Source Code section](#storyboard-agent-full-source).

---

## Stage 2.5: Image Resolver

Automatically downloads images for `image_needed` segments (rapid image lists like "Snoop Dogg, Tom Brady, Paris Hilton") using the Wikipedia REST API.

**CLI:**
```bash
python3 -m pipeline.agents.image_resolver --reel-id my-reel-v1
```

No interactive gate - runs automatically between Storyboard and Veo.

### Source: `pipeline/agents/image_resolver.py`

```python
"""Image Resolver Agent: download images for rapid image list segments via Wikipedia."""

from __future__ import annotations
import argparse, json, os, re, sys, urllib.parse, urllib.request

PIPELINE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_DIR = os.path.dirname(PIPELINE_DIR)
BROLL_DIR = os.path.join(PROJECT_DIR, "public", "broll")
WIKI_API = "https://en.wikipedia.org/api/rest_v1/page/summary"


def _slugify(text: str) -> str:
    slug = text.lower().strip()
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    return slug.strip("-")


def _fetch_wiki_image(query: str) -> str | None:
    title = query.strip().replace(" ", "_")
    url = f"{WIKI_API}/{urllib.parse.quote(title, safe='')}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "ReelPipeline/1.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
            return data.get("originalimage", {}).get("source")
    except Exception as e:
        print(f"    Wikipedia lookup failed for '{query}': {e}")
        return None


def _download_image(url: str, output_path: str) -> bool:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "ReelPipeline/1.0"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, "wb") as f:
                f.write(resp.read())
        return True
    except Exception:
        return False


def resolve_images(storyboard: dict, reel_id: str) -> dict:
    output_dir = os.path.join(BROLL_DIR, "topics", reel_id)
    segments = storyboard.get("segments", [])
    resolved, failed = 0, 0

    for seg in segments:
        if seg.get("type") != "image_needed":
            continue
        query = seg.get("image_query", seg.get("label", ""))
        label = seg.get("label", query)
        slug = _slugify(label)
        if not query:
            failed += 1
            continue

        image_url = _fetch_wiki_image(query)
        if not image_url and " " in query:
            parts = query.split()
            simplified = f"{parts[0]} {parts[-1]}" if len(parts) > 2 else query
            image_url = _fetch_wiki_image(simplified)

        if not image_url:
            failed += 1
            continue

        ext = ".png" if ".png" in image_url.lower() else ".jpg"
        output_path = os.path.join(output_dir, f"{slug}{ext}")
        rel_path = f"topics/{reel_id}/{slug}{ext}"

        if not os.path.exists(output_path):
            if not _download_image(image_url, output_path):
                failed += 1
                continue

        seg["type"] = "screenshot"
        seg["asset_path"] = rel_path
        seg["framing"] = {"objectPosition": "center center", "scaleFrom": 1.0, "scaleTo": 1.08}
        resolved += 1

    return {"resolved": resolved, "failed": failed}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--reel-id", required=True)
    args = parser.parse_args()

    from pipeline.agents.pipeline_state import PipelineState
    state = PipelineState(args.reel_id)
    storyboard = state.get_output("storyboard")
    if not storyboard:
        print("Error: No storyboard found.")
        sys.exit(1)

    result = resolve_images(storyboard, args.reel_id)

    storyboard_path = os.path.join(state.reel_dir, "storyboard.json")
    with open(storyboard_path, "w") as f:
        json.dump(storyboard, f, indent=2)

    print(f"  Resolved: {result['resolved']}, Failed: {result['failed']}")


if __name__ == "__main__":
    main()
```

---

## Stage 3: Veo Agent

Generates AI video clips using Google's Veo 3.1 for storyboard gaps marked as `veo_needed`.

**Models & pricing:**

| Model | Cost/clip | Quality |
|-------|-----------|---------|
| `veo-3.1-fast` | $0.60 | Good (primary choice) |
| `veo-3.1` | $1.60 | Better (hero shots) |
| `veo-3.0-fast` | $0.60 | Decent (budget) |

**CLI:**
```bash
python3 -m pipeline.agents.veo_agent \
  --reel-id my-reel-v1 \
  [--model veo-3.1-fast] \
  [--dry-run]
```

### Veo Generator (`ai-video-exploration/generate_broll.py`)

Create `ai-video-exploration/config.json`:
```json
{
  "gemini_api_key": "YOUR_GOOGLE_API_KEY"
}
```

```python
#!/usr/bin/env python3
"""Generate cinematic B-roll clips using Google Veo via Gemini API."""

from __future__ import annotations
import argparse, json, os, sys, time
from pathlib import Path

from google import genai
from google.genai import types

SCRIPT_DIR = Path(__file__).parent
CONFIG_PATH = SCRIPT_DIR / "config.json"
OUTPUT_DIR = SCRIPT_DIR / "outputs"

MODELS = {
    "veo-3.1-fast": "veo-3.1-fast-generate-preview",
    "veo-3.1": "veo-3.1-generate-preview",
    "veo-3.0-fast": "veo-3.0-fast-generate-001",
}


def generate_clip(client, model_id, prompt, shot_name, variation, output_dir,
                  aspect_ratio="9:16") -> Path | None:
    output_file = output_dir / f"{shot_name}_v{variation}.mp4"
    if output_file.exists():
        return output_file

    print(f"  Generating: {shot_name}_v{variation}")
    try:
        operation = client.models.generate_videos(
            model=model_id, prompt=prompt,
            config=types.GenerateVideosConfig(aspect_ratio=aspect_ratio, number_of_videos=1),
        )
        while not operation.done:
            time.sleep(10)
            operation = client.operations.get(operation)

        if not operation.response or not operation.response.generated_videos:
            return None

        video = operation.response.generated_videos[0]
        video_bytes = client.files.download(file=video.video)
        with open(output_file, "wb") as f:
            f.write(video_bytes)
        return output_file
    except Exception as e:
        print(f"  ERROR: {e}")
        return None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("shot_list", help="Shot list JSON path")
    parser.add_argument("--model", default="veo-3.1-fast", choices=list(MODELS.keys()))
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--yes", "-y", action="store_true")
    args = parser.parse_args()

    with open(CONFIG_PATH) as f:
        config = json.load(f)
    with open(args.shot_list) as f:
        shot_list = json.load(f)

    shots = shot_list.get("shots", [])
    style_prefix = shot_list.get("style_prefix", "")
    cost = len(shots) * {"veo-3.1-fast": 0.60, "veo-3.1": 1.60}.get(args.model, 0.60)

    if args.dry_run:
        for shot in shots:
            print(f"Shot {shot['number']}: {style_prefix} {shot['prompt']}")
        print(f"\nWould generate {len(shots)} clips (~${cost:.2f})")
        return

    if not args.yes:
        if input(f"Generate {len(shots)} clips (~${cost:.2f})? [y/N] ").lower() != "y":
            return

    client = genai.Client(api_key=config["gemini_api_key"])
    run_dir = OUTPUT_DIR / f"{shot_list.get('reel_name', 'reel')}_{time.strftime('%Y%m%d_%H%M%S')}"
    run_dir.mkdir(parents=True, exist_ok=True)

    for i, shot in enumerate(shots):
        full_prompt = f"{style_prefix} {shot['prompt']}".strip()
        if i > 0:
            print(f"  Waiting 60s (rate limit)...")
            time.sleep(60)
        generate_clip(client, MODELS[args.model], full_prompt,
                      f"shot{shot['number']:02d}_{shot['name']}", 1, run_dir)

    print(f"\nDone! Output: {run_dir}")


if __name__ == "__main__":
    main()
```

---

## Stage 4: Assembly

Converts the storyboard into a final ReelConfig JSON for Remotion, validates everything, and optionally renders.

**Validation checks (blocks on errors):**
1. No PLACEHOLDERs in asset paths
2. No gaps > 0.1s between segments
3. No text duplication
4. No dark/low-quality assets
5. All referenced files exist on disk
6. Caption chunks present

**CLI:**
```bash
python3 -m pipeline.agents.assembly \
  --reel-id my-reel-v1 \
  [--render] \
  [--crossfade 5] \
  [--avatar-margin -280]
```

---

## Stage 5: Review

Post-render quality verification. Extracts key frames at each segment boundary, analyzes brightness, detects black frames, and checks semantic relevance.

**Checks:**
1. Duration match (rendered vs config)
2. Audio presence
3. Per-segment frame extraction and brightness analysis
4. Variance-aware black frame detection (distinguishes dark UI content from truly black frames)
5. B-roll semantic relevance
6. Face-only section check

**CLI:**
```bash
python3 -m pipeline.agents.reviewer \
  --reel-id my-reel-v1 \
  [--rendered out/my-reel-v1.mp4]
```

**Verdicts:** pass / warn / fail. On fail, loop back to storyboard or assembly (max 3 iterations).

---

## Pipeline State Manager

Tracks progress across all stages. Every reel gets a state directory.

### Source: `pipeline/agents/pipeline_state.py`

```python
"""Pipeline State Manager: tracks per-reel progress across agent stages."""

import json
import os
from datetime import datetime, timezone

PIPELINE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(PIPELINE_DIR, "output")
STAGES = ["curate", "storyboard", "veo", "assemble", "review"]


class PipelineState:
    def __init__(self, reel_id: str):
        self.reel_id = reel_id
        self._dir = os.path.join(OUTPUT_DIR, reel_id)
        self._state_path = os.path.join(self._dir, "pipeline-state.json")
        self._data = self._load()

    @property
    def reel_dir(self) -> str:
        return self._dir

    def _load(self) -> dict:
        if os.path.exists(self._state_path):
            with open(self._state_path) as f:
                return json.load(f)
        return {}

    def _now(self) -> str:
        return datetime.now(timezone.utc).isoformat()

    def exists(self) -> bool:
        return bool(self._data)

    def init(self, tool_name: str, transcript_path: str = "",
             avatar_src: str = "", script: str = "", product_url: str = ""):
        os.makedirs(self._dir, exist_ok=True)
        os.makedirs(os.path.join(self._dir, "frames"), exist_ok=True)
        self._data = {
            "reel_id": self.reel_id, "created": self._now(), "updated": self._now(),
            "tool_name": tool_name, "transcript_path": transcript_path,
            "avatar_src": avatar_src, "script": script, "product_url": product_url,
            "speed_factor": 1.1,
            "stages": {stage: {"status": "pending"} for stage in STAGES},
            "iteration": 1, "history": [],
        }
        self.save()

    def get_stage_status(self, stage: str) -> str:
        return self._data.get("stages", {}).get(stage, {}).get("status", "pending")

    def complete_stage(self, stage: str, output_filename: str, summary: dict):
        output_path = os.path.join(self._dir, output_filename)
        stages = self._data.setdefault("stages", {})
        stages[stage] = {
            "status": "completed", "completed_at": self._now(),
            "output_path": output_path, "summary": summary,
        }
        self._data["updated"] = self._now()
        self.save()

    def approve_gate(self, stage: str):
        stages = self._data.get("stages", {})
        if stage in stages:
            stages[stage]["status"] = "approved"
            stages[stage]["approved_at"] = self._now()
            self._data["updated"] = self._now()
            self.save()

    def get_output(self, stage: str) -> dict:
        stage_data = self._data.get("stages", {}).get(stage, {})
        output_path = stage_data.get("output_path", "")
        if output_path and os.path.exists(output_path):
            with open(output_path) as f:
                return json.load(f)
        return {}

    def get_config(self, key: str, default=None):
        return self._data.get(key, default)

    def save(self):
        os.makedirs(self._dir, exist_ok=True)
        with open(self._state_path, "w") as f:
            json.dump(self._data, f, indent=2)

    def summary(self) -> str:
        lines = [f"Reel: {self.reel_id}", f"Tool: {self._data.get('tool_name', '?')}", ""]
        for stage in STAGES:
            status = self.get_stage_status(stage)
            lines.append(f"  {stage:<12} {status}")
        return "\n".join(lines)


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("reel_id")
    parser.add_argument("--init", action="store_true")
    parser.add_argument("--tool", help="Tool name (required for --init)")
    parser.add_argument("--transcript", default="")
    parser.add_argument("--avatar", default="")
    parser.add_argument("--script", default="")
    parser.add_argument("--url", default="")
    args = parser.parse_args()

    state = PipelineState(args.reel_id)
    if args.init:
        if not args.tool:
            print("Error: --tool required for --init")
            return
        state.init(tool_name=args.tool, transcript_path=args.transcript,
                   avatar_src=args.avatar, script=args.script, product_url=args.url)
        print(f"Initialized pipeline for: {args.reel_id}")

    if state.exists():
        print(state.summary())
    else:
        print(f"No pipeline found for: {args.reel_id}")


if __name__ == "__main__":
    main()
```

---

## Remotion Rendering System

The rendering layer is built with [Remotion](https://remotion.dev) - a React framework for programmatic video.

### Constants (`src/lib/constants.ts`)

```typescript
export const FPS = 25;
export const WIDTH = 1080;
export const HEIGHT = 1920;
export const TOP_HEIGHT = 960;
export const BOTTOM_HEIGHT = 960;

export const COLORS = {
  darkBg: '#080808',
  lightBg: '#EAEAEA',
  white: '#FFFFFF',
  accent: '#6C63FF',
  green: '#2ECC9A',
  red: '#E8445A',
  amber: '#FFB800',
  divider: 'rgba(255, 255, 255, 0.25)',
};

export const secToFrame = (sec: number) => Math.round(sec * FPS);

export const FONT = {
  family: '"Inter", system-ui, sans-serif',
  headline: { fontSize: 58, fontWeight: 800 as const, letterSpacing: '-0.03em', lineHeight: 1.18 },
  body: { fontSize: 42, fontWeight: 600 as const, letterSpacing: '-0.01em', lineHeight: 1.3 },
  label: { fontSize: 28, fontWeight: 700 as const, letterSpacing: '0.05em', lineHeight: 1.4 },
};
```

### TypeScript Interfaces (`src/lib/dynamic-config.ts`)

```typescript
export interface BRollSegment {
  video?: string;       // Filename in public/broll/clips/
  image?: string;       // Filename in public/broll/ or public/broll/topics/
  startSec: number;
  endSec: number;
  objectPosition?: string;  // CSS object-position (default 'center center')
  scaleFrom?: number;       // Ken Burns start zoom (default 1.0)
  scaleTo?: number;         // Ken Burns end zoom (default 1.05)
  videoStartSec?: number;   // Skip into source video
  objectFit?: 'cover' | 'contain';
}

export interface CaptionChunk {
  text: string;
  startSec: number;
  endSec: number;
}

export type SceneType = 'hook' | 'bullets' | 'featureGrid' | 'bigNumber' |
  'contrast' | 'strikethrough' | 'logoGrid' | 'closing';

export interface SceneConfig {
  type: SceneType;
  startSec: number;
  endSec: number;
  params: Record<string, unknown>;
}

export interface ReelConfig {
  id: string;
  duration: number;          // Frames at 25fps
  avatarSrc: string;         // In public/
  avatarMarginTop?: number;  // Vertical crop offset (default -280)
  brollSegments: BRollSegment[];
  captionChunks: CaptionChunk[];
  scenes: SceneConfig[];
  crossfadeFrames?: number;  // Transition frames (default 8)
}
```

### Main Composition (`src/DynamicReel.tsx`)

```tsx
import React from 'react';
import { AbsoluteFill, staticFile } from 'remotion';
import { Video } from '@remotion/media';
import { COLORS, TOP_HEIGHT, BOTTOM_HEIGHT } from './lib/constants';
import type { ReelConfig } from './lib/dynamic-config';
import { DynamicBRoll } from './components/DynamicBRoll';
import { DynamicCaptionOverlay } from './components/DynamicCaptionOverlay';
import { DynamicSceneRenderer } from './components/DynamicSceneRenderer';

export const DynamicReel: React.FC<{ config: ReelConfig }> = ({ config }) => {
  const avatarMarginTop = config.avatarMarginTop ?? -280;
  return (
    <AbsoluteFill style={{ backgroundColor: COLORS.darkBg }}>
      {/* TOP HALF: B-roll + scenes */}
      <div style={{
        position: 'absolute', top: 0, left: 0, width: '100%',
        height: TOP_HEIGHT, overflow: 'hidden',
      }}>
        <DynamicBRoll segments={config.brollSegments} crossfadeFrames={config.crossfadeFrames} />
        <DynamicSceneRenderer scenes={config.scenes} />
      </div>

      {/* DIVIDER */}
      <div style={{
        position: 'absolute', top: TOP_HEIGHT, left: 0, width: '100%',
        height: 2, background: COLORS.divider, zIndex: 10,
      }} />

      {/* CAPTIONS */}
      <DynamicCaptionOverlay chunks={config.captionChunks} topOffset={TOP_HEIGHT} />

      {/* BOTTOM HALF: Avatar */}
      <div style={{
        position: 'absolute', top: TOP_HEIGHT + 2, left: 0, width: '100%',
        height: BOTTOM_HEIGHT - 2, overflow: 'hidden', backgroundColor: '#000000',
        display: 'flex', alignItems: 'flex-start', justifyContent: 'center',
      }}>
        <Video
          src={staticFile(config.avatarSrc)}
          style={{ width: '100%', height: 'auto', marginTop: avatarMarginTop }}
        />
      </div>
    </AbsoluteFill>
  );
};
```

### B-Roll Renderer (`src/components/DynamicBRoll.tsx`)

```tsx
import React from 'react';
import { useCurrentFrame, interpolate, Sequence, staticFile, OffthreadVideo, Img } from 'remotion';
import { FPS, TOP_HEIGHT, secToFrame } from '../lib/constants';
import type { BRollSegment } from '../lib/dynamic-config';

export const DynamicBRoll: React.FC<{
  segments: BRollSegment[];
  crossfadeFrames?: number;
}> = ({ segments, crossfadeFrames }) => {
  const frame = useCurrentFrame();
  const CF = crossfadeFrames ?? 8;

  return (
    <div style={{
      position: 'absolute', top: 0, left: 0, width: '100%',
      height: TOP_HEIGHT, overflow: 'hidden', backgroundColor: '#080808',
    }}>
      {segments.map((seg, i) => {
        const startFrame = secToFrame(seg.startSec);
        const endFrame = secToFrame(seg.endSec);

        if (frame < startFrame - CF || frame > endFrame + CF) return null;

        const fadeIn = interpolate(frame, [startFrame, startFrame + CF], [0, 1],
          { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
        const fadeOut = interpolate(frame, [endFrame - CF, endFrame], [1, 0],
          { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
        const opacity = Math.min(fadeIn, fadeOut);
        if (opacity <= 0) return null;

        const progress = interpolate(frame, [startFrame, endFrame], [0, 1],
          { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
        const scaleFrom = seg.scaleFrom ?? 1.0;
        const scaleTo = seg.scaleTo ?? 1.05;
        const scale = scaleFrom + (scaleTo - scaleFrom) * progress;

        const seqStart = Math.max(0, startFrame - CF);
        const seqDuration = endFrame + CF - seqStart;

        const fit = seg.objectFit || 'cover';
        const mediaStyle: React.CSSProperties = {
          width: '100%', height: '100%', objectFit: fit,
          objectPosition: seg.objectPosition || 'center center',
          transform: `scale(${scale})`, transformOrigin: 'center center',
          ...(fit === 'contain' ? { padding: '15%' } : {}),
        };

        return (
          <div key={`broll-${i}`} style={{
            position: 'absolute', top: 0, left: 0, width: '100%', height: '100%', opacity,
          }}>
            {seg.video ? (
              <Sequence from={seqStart} durationInFrames={seqDuration} layout="none">
                <OffthreadVideo
                  src={staticFile(`broll/clips/${seg.video}`)}
                  startFrom={seg.videoStartSec ? Math.round(seg.videoStartSec * FPS) : undefined}
                  style={mediaStyle} muted
                />
              </Sequence>
            ) : seg.image ? (
              <Img src={staticFile(`broll/${seg.image}`)} style={mediaStyle} />
            ) : null}
          </div>
        );
      })}
      {/* Vignette */}
      <div style={{
        position: 'absolute', top: 0, left: 0, width: '100%', height: '100%',
        background: 'radial-gradient(ellipse at center, transparent 50%, rgba(0,0,0,0.3) 100%)',
        pointerEvents: 'none',
      }} />
    </div>
  );
};
```

### Caption Overlay (`src/components/DynamicCaptionOverlay.tsx`)

```tsx
import React from 'react';
import { useCurrentFrame, interpolate } from 'remotion';
import { FONT, secToFrame } from '../lib/constants';
import type { CaptionChunk } from '../lib/dynamic-config';

export const DynamicCaptionOverlay: React.FC<{
  chunks: CaptionChunk[];
  topOffset: number;
}> = ({ chunks, topOffset }) => {
  const frame = useCurrentFrame();

  let activeChunk: CaptionChunk | null = null;
  for (const chunk of chunks) {
    if (frame >= secToFrame(chunk.startSec) && frame < secToFrame(chunk.endSec)) {
      activeChunk = chunk;
      break;
    }
  }
  if (!activeChunk) return null;

  const startFrame = secToFrame(activeChunk.startSec);
  const endFrame = secToFrame(activeChunk.endSec);

  const scaleIn = interpolate(frame, [startFrame, startFrame + 3], [0.7, 1.0],
    { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  const opacityIn = interpolate(frame, [startFrame, startFrame + 2], [0, 1],
    { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  const opacityOut = interpolate(frame, [endFrame - 2, endFrame], [1, 0],
    { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });

  return (
    <div style={{
      position: 'absolute', top: topOffset - 32, left: 0, width: '100%',
      display: 'flex', justifyContent: 'center', zIndex: 100, pointerEvents: 'none',
    }}>
      <div style={{
        opacity: Math.min(opacityIn, opacityOut), transform: `scale(${scaleIn})`,
        background: 'linear-gradient(135deg, #C030E0, #9B30FF)',
        borderRadius: 16, paddingLeft: 32, paddingRight: 32, paddingTop: 12, paddingBottom: 14,
        boxShadow: '0 4px 20px rgba(155, 48, 255, 0.4), 0 2px 8px rgba(0,0,0,0.3)',
      }}>
        <div style={{
          color: '#FFFFFF', fontFamily: FONT.family, fontSize: 50, fontWeight: 800,
          letterSpacing: '-0.01em', lineHeight: 1.1, textAlign: 'center',
          textShadow: '0 2px 4px rgba(0,0,0,0.3)', whiteSpace: 'nowrap',
        }}>
          {activeChunk.text}
        </div>
      </div>
    </div>
  );
};
```

### Root Composition (`src/Root.tsx`)

```tsx
import React from 'react';
import { Composition } from 'remotion';
import { DynamicReel } from './DynamicReel';
import { FPS, WIDTH, HEIGHT } from './lib/constants';
import type { ReelConfig } from './lib/dynamic-config';

const defaultConfig: ReelConfig = {
  id: 'preview', duration: 750, avatarSrc: 'avatar-preview.mp4',
  avatarMarginTop: -280, brollSegments: [], captionChunks: [], scenes: [],
};

export const Root: React.FC = () => (
  <Composition
    id="DynamicReel"
    component={DynamicReel}
    durationInFrames={750}
    width={WIDTH}
    height={HEIGHT}
    fps={FPS}
    defaultProps={{ config: defaultConfig }}
    calculateMetadata={({ props }) => ({
      durationInFrames: props.config?.duration ?? 750,
    })}
  />
);
```

### Rendering Commands

```bash
# Create props file (wraps config as {"config": ...})
python3 -c "
import json
config = json.load(open('public/config/reel-config-my-reel.json'))
json.dump({'config': config}, open('/tmp/reel-props.json', 'w'))
"

# Render
npx remotion render DynamicReel out/my-reel.mp4 --codec=h264 --props=/tmp/reel-props.json

# Verify
ffprobe out/my-reel.mp4  # Check duration matches config
```

---

## JSON Config Schema

Every reel is defined by a single JSON file. This is the contract between the pipeline and the renderer.

```json
{
  "id": "my-reel-v1",
  "duration": 853,
  "avatarSrc": "avatars/avatar-my-reel.mp4",
  "avatarMarginTop": -280,
  "crossfadeFrames": 5,
  "brollSegments": [
    {
      "image": "topics/my-product/hero-screenshot.png",
      "startSec": 0,
      "endSec": 2.4,
      "objectPosition": "center 25%",
      "scaleFrom": 1.0,
      "scaleTo": 1.05,
      "_speech": "What the avatar says here (annotation only)"
    },
    {
      "video": "product-demo-clip.mp4",
      "startSec": 2.4,
      "endSec": 5.0,
      "objectPosition": "center 65%",
      "scaleFrom": 1.25,
      "scaleTo": 1.3,
      "videoStartSec": 2,
      "_speech": "See how easy it is to..."
    }
  ],
  "captionChunks": [
    { "text": "This product", "startSec": 0.0, "endSec": 0.8 },
    { "text": "just changed", "startSec": 0.8, "endSec": 1.5 },
    { "text": "everything.", "startSec": 1.5, "endSec": 2.4 }
  ],
  "scenes": []
}
```

**Key fields:**
- `duration`: Total frames at 25fps (e.g., 853 frames = 34.12 seconds)
- `avatarMarginTop`: Negative values shift the avatar video up (showing more head/torso)
- `crossfadeFrames`: 3=snappy, 5=smooth (recommended), 8=cinematic
- `_speech`: Annotation only, not rendered - helps with semantic matching during editing

---

## Claude Code Integration

To orchestrate this pipeline through Claude Code, create a slash command:

### `.claude/commands/reels.md`

```markdown
# Reels Pipeline

Orchestrate the staged reel production pipeline. Request: $ARGUMENTS

Read the pipeline agents documentation for full details on each stage.

---

## Critical Rules

1. **Max 45 seconds.** Scripts must fit within 45 seconds.
2. **Never double-scale timestamps.** When Whisper runs on the sped-up avatar,
   timestamps are already correct.
3. **No scene overlays.** The `scenes` array must always be empty.
4. **B-roll must match speech.** Every segment must be semantically relevant.

---

## Commands

Parse `$ARGUMENTS` to determine the action:

- **`new <name> --script "text" --avatar <path>`** - Initialize pipeline
- **`curate <reel-id>`** - Run Asset Curator, present manifest, wait for approval
- **`storyboard <reel-id>`** - Run Storyboard Agent, present timeline, wait for approval
- **`veo <reel-id>`** - Generate Veo clips if needed
- **`assemble <reel-id> [--render]`** - Build config + render
- **`review <reel-id>`** - Post-render QA check
- **`status <reel-id>`** - Show pipeline state
- **`full <reel-id>`** - Run all stages with gates

---

## Working Directory

All scripts run from the reels project root:
```bash
python3 -m pipeline.agents.<agent_name> --reel-id <id> [options]
```
```

---

## Design Principles

1. **Max 45 seconds** - Short attention spans. Write tighter scripts.
2. **Whisper on sped-up video** - Timestamps are inherently correct. Never double-scale.
3. **Duration from ffprobe** - Use actual video duration, not transcript word timestamps.
4. **Fast cuts, high energy** - 10-15 segments, most 1.5-2.5s. Video > static.
5. **Semantic B-roll** - Every visual must relate to what's being said at that moment.
6. **Quality gates** - Human approval between stages prevents bad reels from rendering.
7. **Fix loops** - On review failure, loop back (max 3 iterations) rather than starting over.
8. **JSON-driven** - No new React code per reel. Everything is data.

---

## Troubleshooting

### Common Issues

| Problem | Cause | Fix |
|---------|-------|-----|
| Black frames in render | Missing B-roll asset file | Check paths in reel-config.json match actual files |
| Audio/video desync | Double-scaled timestamps | Only scale if transcript is from original (non-sped) video |
| Dark frames flagged | Terminal/code screenshots | Reviewer uses variance-aware detection - dark content with text is OK |
| Assembly validation fails | Unresolved PLACEHOLDERs | Run image resolver and veo agent first |
| Render crashes | Missing Remotion deps | Run `npm install` in project root |
| Veo rate limited | Too many requests | 60s delay between clips (tier 1 limit) |

### FFmpeg Quick Reference

```bash
# Speed up video 1.1x with pitch preservation
ffmpeg -i input.mp4 \
  -filter_complex "[0:v]setpts=PTS/1.1[v];[0:a]atempo=1.1[a]" \
  -map "[v]" -map "[a]" -c:v libx264 -preset fast -crf 18 -c:a aac -b:a 192k \
  output.mp4

# Extract frame at specific timestamp
ffmpeg -ss 5 -i video.mp4 -frames:v 1 -q:v 2 frame-5s.jpg

# Get video duration
ffprobe -v quiet -show_entries format=duration -of csv=p=0 video.mp4

# Get brightness
ffmpeg -i image.png -vf signalstats -f null - 2>&1 | grep YAVG

# Trim a clip
ffmpeg -ss 5 -t 3 -i raw.mp4 -an -c:v libx264 -crf 18 trimmed.mp4
```

---

## License

This pipeline is shared as a free resource. Use it however you want. No attribution required.

Built with Claude Code, Remotion, HeyGen, Google Veo, and Whisper.
