#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
SCRIPT: batch_whisper_subtitles.py
DESCRIPTION:
  This script automates subtitle generation for all .mp4 files in the directory
  using Whisper AI and embeds them using FFmpeg, with asynchronous processing.

FEATURES:
  - Converts filenames to snake-case with hyphens
  - Automatically checks for required dependencies
  - Processes subtitles in English only (modifiable)
  - Cleans up only Whisper-generated files (srt, tsv, txt, vtt, json) **immediately after embedding**
  - Uses asynchronous processing for better performance

USAGE:
  1. Install dependencies: pip install openai-whisper aiofiles tqdm
  2. Run for all MP4 files: python batch_whisper_subtitles.py
"""

import asyncio
import concurrent.futures
import glob
import importlib.util
import os
import re
import subprocess
import sys
from typing import Optional, Tuple

# Default settings
WHISPER_LANG = "English"
MODEL = "base"  # Options: "small", "tiny", "medium", "large"
MAX_WORKERS = os.cpu_count()  # Use all available CPU cores for parallel processing


class Colors:
    """Class for formatting colored text in terminal."""
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    RESET = '\033[0m'


def print_colored(text: str, color: str):
    """Print colored text to terminal."""
    print(f"{color}{text}{Colors.RESET}")


async def check_dependencies() -> bool:
    """Check and install required dependencies."""
    print_colored("🔍 Checking for required dependencies...", Colors.BLUE)

    required_cmds = ["python3", "ffmpeg"]
    missing_cmds = []

    for cmd in required_cmds:
        try:
            subprocess.run(
                [cmd, "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except FileNotFoundError:
            missing_cmds.append(cmd)

    if missing_cmds:
        print_colored(
            f"❌ Missing dependencies: {', '.join(missing_cmds)}", Colors.RED)
        print("Please install them manually and run the script again.")
        return False

    for pkg in ["whisper", "tqdm", "aiofiles"]:
        if importlib.util.find_spec(pkg) is None:
            print_colored(f"🔧 Installing {pkg}...", Colors.YELLOW)
            subprocess.run([sys.executable, "-m", "pip", "install", pkg])

    print_colored("✅ All dependencies are installed.", Colors.GREEN)
    return True


def to_snake_case(filename: str) -> str:
    """Convert filenames to lowercase with hyphens."""
    filename = filename.rsplit('.', 1)[0]  # Remove extension
    return re.sub(r'[^a-z0-9]+', '-', filename.lower()).strip('-')


def format_timestamp(seconds: float) -> str:
    """Format seconds to SRT timestamp format (HH:MM:SS,mmm)."""
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)
    milliseconds = int((seconds - int(seconds)) * 1000)
    return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d},{milliseconds:03d}"


def run_whisper_process(video_file: str, model_name: str, language: str) -> str:
    """Run Whisper in a separate process."""
    try:
        import whisper
        model = whisper.load_model(model_name)
        result = model.transcribe(
            video_file, language=language, task="translate")

        output_file = os.path.splitext(video_file)[0] + ".srt"
        with open(output_file, "w", encoding="utf-8") as f:
            for i, segment in enumerate(result["segments"]):
                f.write(
                    f"{i+1}\n{format_timestamp(segment['start'])} --> {format_timestamp(segment['end'])}\n{segment['text'].strip()}\n\n")

        return output_file
    except Exception as e:
        print(f"Error processing {video_file}: {str(e)}")
        return ""


async def embed_subtitles(video_file: str, srt_file: str) -> Optional[str]:
    """Embed subtitles into the video using FFmpeg."""
    try:
        output_file = f"{to_snake_case(video_file)}_subtitled_en_us.mp4"
        process = await asyncio.create_subprocess_exec(
            "ffmpeg", "-i", video_file, "-vf", f"subtitles={srt_file}",
            "-c:a", "copy", output_file,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        await process.communicate()
        return output_file if os.path.exists(output_file) else None
    except Exception as e:
        print_colored(
            f"❌ Error embedding subtitles in {video_file}: {str(e)}", Colors.RED)
        return None


async def clean_whisper_files_for_video(video_file: str):
    """Remove Whisper-generated files for a specific video."""
    base_name = os.path.splitext(video_file)[0]
    for ext in [".srt", ".tsv", ".txt", ".vtt", ".json"]:
        file_to_delete = f"{base_name}{ext}"
        if os.path.exists(file_to_delete):
            os.remove(file_to_delete)
            print_colored(f"🗑️ Removed: {file_to_delete}", Colors.GREEN)


async def process_video(video_file: str, semaphore: asyncio.Semaphore, executor: concurrent.futures.ProcessPoolExecutor) -> Tuple[bool, str]:
    """Process a single video file: generate subtitles and embed them."""
    async with semaphore:
        print_colored(f"🎬 Processing: {video_file}", Colors.BLUE)

        try:
            srt_file = await asyncio.get_event_loop().run_in_executor(executor, run_whisper_process, video_file, MODEL, WHISPER_LANG)
            if not srt_file or not os.path.exists(srt_file):
                return False, video_file

            print_colored(
                f"✅ Subtitle file generated: {srt_file}", Colors.GREEN)
            output_file = await embed_subtitles(video_file, srt_file)

            if output_file:
                await clean_whisper_files_for_video(video_file)
                print_colored(
                    f"✅ Subtitled video saved: {output_file}", Colors.GREEN)
                return True, video_file
            return False, video_file
        except Exception as e:
            print_colored(f"❌ Error: {str(e)}", Colors.RED)
            return False, video_file


async def main():
    """Main function to coordinate asynchronous video processing."""
    if not await check_dependencies():
        return

    video_files = glob.glob("*.mp4")
    if not video_files:
        print_colored("❌ No MP4 files found.", Colors.RED)
        return

    print_colored(f"🔍 Found {len(video_files)} videos.", Colors.BLUE)
    max_concurrent = min(MAX_WORKERS, 6)
    semaphore = asyncio.Semaphore(max_concurrent)

    with concurrent.futures.ProcessPoolExecutor(max_workers=max_concurrent) as executor:
        tasks = [process_video(video, semaphore, executor)
                 for video in video_files]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
