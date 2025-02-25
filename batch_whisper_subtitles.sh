#!/bin/bash

# =====================================================
# SCRIPT: batch_whisper_subtitles.sh
# DESCRIPTION:
#   This script automates subtitle generation for all .mp4 files in the directory
#   using Whisper AI and embeds them using FFmpeg.
#
# FEATURES:
#   - Converts filenames to snake-case with hyphens
#   - Automatically checks for required dependencies
#   - Processes subtitles in English only (modifiable)
#   - Cleans up only Whisper-generated files (srt, tsv, txt, vtt, json)
#
# USAGE:
#   1. Give execution permission: chmod +x batch_whisper_subtitles.sh
#   2. Run for all MP4 files: ./batch_whisper_subtitles.sh
#
# =====================================================

# Enable debugging mode (uncomment for testing)
# set -x

# Function to check and install dependencies
check_and_install_dependencies() {
    echo "🔍 Checking for required dependencies..."

    # List of required commands
    REQUIRED_CMDS=("python3" "ffmpeg" "iconv")

    for cmd in "${REQUIRED_CMDS[@]}"; do
        if ! command -v $cmd &>/dev/null; then
            echo "❌ Missing dependency: $cmd"
            echo "Please install it manually and rerun the script."
            exit 1
        fi
    done

    # Check if Whisper is installed in Python
    if ! python3 -c "import whisper" &>/dev/null; then
        echo "❌ Missing Python module: whisper"
        echo "Installing Whisper..."
        pip install openai-whisper
    fi

    echo "✅ All dependencies are installed."
}

# Check dependencies before running
check_and_install_dependencies

# Set the default language for Whisper (English)
WHISPER_LANG="English" # To change this, check available languages at: https://github.com/openai/whisper/blob/main/whisper/tokenizer.py#L10

# Define the Whisper model (adjustable)
MODEL="base" # Change to "small", "tiny", "medium", or "large" if needed

# Function to convert filenames to snake-case with hyphens
to_snake_case() {
    echo "$1" | tr '[:upper:]' '[:lower:]' | sed -E 's/[^a-z0-9]+/-/g' | sed -E 's/^-|-$//g'
}

# Get the total number of files
TOTAL_FILES=$(ls *.mp4 2>/dev/null | wc -l)
CURRENT_FILE=0

# Process each video file
for VIDEO in *.mp4; do
    CURRENT_FILE=$((CURRENT_FILE + 1))

    BASENAME="${VIDEO%.*}" # Remove file extension
    SNAKE_NAME=$(to_snake_case "$BASENAME")
    OUTPUT_FILE="${SNAKE_NAME}_subtitled_en_us.mp4"

    echo "🔹 Processing file $CURRENT_FILE of $TOTAL_FILES: $VIDEO"

    # Generate subtitles with Whisper
    echo "🎙️ Generating subtitles in English..."
    whisper "$VIDEO" --language "$WHISPER_LANG" --task translate --model "$MODEL" --output_format srt

    # Find the exact generated .srt filename
    SRT_FILE=$(ls *.srt | grep -i "$BASENAME" | head -n 1)

    # If not found, try with snake-case
    if [ -z "$SRT_FILE" ]; then
        SRT_FILE=$(ls *.srt | grep -i "$SNAKE_NAME" | head -n 1)
    fi

    # If still not found, display an error and continue
    if [ -z "$SRT_FILE" ]; then
        echo "❌ Error: Subtitle file not found for $VIDEO"
        continue
    fi

    echo "✅ Subtitle file found: $SRT_FILE"

    # Convert the subtitle file to UTF-8 encoding
    iconv -f UTF-8 -t UTF-8 "$SRT_FILE" -o "$SRT_FILE"

    # Embed subtitles into the video using FFmpeg
    ffmpeg -i "$VIDEO" -vf "subtitles=$SRT_FILE" -c:a copy "$OUTPUT_FILE"

    # Verify if the video was successfully created
    if [ -f "$OUTPUT_FILE" ]; then
        echo "✅ Subtitled video saved as: $OUTPUT_FILE"
    else
        echo "❌ Error creating subtitled video for: $VIDEO"
    fi
done

# Remove only Whisper-generated files
echo "🗑️ Cleaning up Whisper-generated files..."
find . -type f \( -name "*.srt" -o -name "*.tsv" -o -name "*.txt" -o -name "*.vtt" -o -name "*.json" \) -delete
echo "✅ Cleanup complete!"
