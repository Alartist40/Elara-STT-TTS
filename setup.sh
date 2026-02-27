#!/bin/bash
# Elara Mini Setup Script

set -e

echo "Installing Elara Mini..."

# Check Python version
python3 --version || { echo "Python 3 not found"; exit 1; }

# Check Go is installed
if ! command -v go &> /dev/null; then
    echo "ERROR: Go not found. Install: sudo pacman -S go"
    exit 1
fi

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Download Piper binary (Linux x64)
if [ ! -d "piper" ]; then
    echo "Downloading Piper TTS..."
    wget -q https://github.com/rhasspy/piper/releases/download/v1.2.0/piper_amd64.tar.gz
    tar -xzf piper_amd64.tar.gz
    rm piper_amd64.tar.gz
    echo "Piper downloaded"
fi

# Download voice model
mkdir -p models
if [ ! -f "models/en_US-lessac-medium.onnx" ]; then
    echo "Downloading voice model..."
    wget -q -O models/en_US-lessac-medium.onnx \
        https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/lessac/medium/en_US-lessac-medium.onnx
    wget -q -O models/en_US-lessac-medium.onnx.json \
        https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/lessac/medium/en_US-lessac-medium.onnx.json
    echo "Voice model downloaded"
fi

# Check system dependencies
echo "Checking system dependencies..."
if ! command -v arecord &> /dev/null && ! command -v rec &> /dev/null; then
    echo "WARNING: No audio recorder found. Install: sudo pacman -S alsa-utils sox"
fi

if ! command -v aplay &> /dev/null; then
    echo "WARNING: No audio player found. Install: sudo pacman -S alsa-utils"
fi

if ! command -v espeak &> /dev/null; then
    echo "WARNING: espeak not found (fallback TTS). Install: sudo pacman -S espeak"
fi

# Build Go binary
echo "Building Elara..."
go build -o elara main.go

echo ""
echo "Setup complete. Run: ./elara"