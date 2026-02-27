#!/usr/bin/env python3
import sys
import argparse
import tempfile
import wave
import subprocess
import os

# Lazy load whisper
_whisper_model = None

def get_model(size="tiny"):
    global _whisper_model
    if _whisper_model is None:
        import whisper
        _whisper_model = whisper.load_model(size)
    return _whisper_model

def record_audio(duration=5, output_path=None):
    """Record audio using arecord (Linux) or sox."""
    if output_path is None:
        fd, output_path = tempfile.mkstemp(suffix=".wav")
        os.close(fd)
    
    # Try arecord first (ALSA), fallback to sox
    cmd = [
        "arecord", "-d", str(duration), "-f", "cd", "-t", "wav",
        "-q", output_path
    ]
    
    try:
        subprocess.run(cmd, check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        # Fallback to sox rec
        cmd = ["rec", "-q", "-r", "16000", "-c", "1", output_path, "trim", "0", str(duration)]
        subprocess.run(cmd, check=True)
    
    return output_path

def transcribe(audio_path, model_size="tiny"):
    model = get_model(model_size)
    result = model.transcribe(audio_path)
    return result["text"].strip()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--duration", type=int, default=5)
    parser.add_argument("--model", default="tiny")
    parser.add_argument("--file", help="Existing audio file to transcribe")
    args = parser.parse_args()

    try:
        if args.file:
            text = transcribe(args.file, args.model)
        else:
            print("[recording...]", file=sys.stderr)
            audio_path = record_audio(args.duration)
            text = transcribe(audio_path, args.model)
            os.remove(audio_path)
        
        print(text)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()