#!/usr/bin/env python3
import sys
import argparse
import subprocess
import tempfile
import os

def speak(text, speed=1.0):
    """
    Text-to-speech using Piper (local, fast, small models).
    Falls back to espeak if piper not available.
    """
    
    # Path to local piper binary (relative to script location)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    piper_path = os.path.join(script_dir, "..", "piper", "piper")
    model_path = os.path.join(script_dir, "..", "models", "en_US-lessac-medium.onnx")
    
    # Check if local piper exists and works
    if os.path.exists(piper_path) and os.path.exists(model_path):
        _piper_speak(text, piper_path, model_path, speed)
    elif _command_exists("espeak"):
        _espeak_speak(text, speed)
    else:
        print(f"[TTS] {text}", file=sys.stderr)

def _piper_speak(text, piper_path, model_path, speed):
    """Piper TTS with local binary"""
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        wav_path = f.name
    
    # Generate audio using local piper
    echo = subprocess.Popen(["echo", text], stdout=subprocess.PIPE)
    piper = subprocess.Popen(
        [piper_path, "--model", model_path, "--output_file", wav_path],
        stdin=echo.stdout,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    piper.wait()
    
    # Play audio
    _play_audio(wav_path)
    os.remove(wav_path)

def _espeak_speak(text, speed):
    """Fallback espeak"""
    wpm = int(175 * speed)
    subprocess.run(["espeak", "-s", str(wpm), text], 
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def _play_audio(wav_path):
    """Play wav file using available player"""
    players = ["aplay", "paplay", "ffplay", "afplay"]
    for player in players:
        if _command_exists(player):
            subprocess.run([player, wav_path], 
                          stdout=subprocess.DEVNULL, 
                          stderr=subprocess.DEVNULL)
            return

def _command_exists(cmd):
    """Check if command exists in PATH"""
    return subprocess.run(
        ["which", cmd], 
        stdout=subprocess.DEVNULL, 
        stderr=subprocess.DEVNULL
    ).returncode == 0

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("text", help="Text to speak")
    parser.add_argument("--speed", type=float, default=1.0)
    args = parser.parse_args()

    speak(args.text, args.speed)

if __name__ == "__main__":
    main()