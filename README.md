  **setup.sh placement:** Root directory (same level as `main.go`, `elara` binary). Your structure looks correct.

---

**README.md**

```markdown
# Elara Mini

A lightweight, offline IT assistant for old and small devices. 4GB RAM target. No cloud dependencies.

## What It Does

- **Text/Voice Input:** Type normally or press `@` to speak
- **AI Response:** Local LLM (TinyLlama 1.1B) generates answers
- **Voice Output:** Piper TTS speaks the response aloud
- **Use Case:** System administration help without internet or heavy resources

## Architecture

┌─────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐
│  User   │────→│  Go Main │────→│  Python  │────→│  Piper   │
│ Input   │     │  Loop    │     │  Model   │     │  TTS     │
└─────────┘     └──────────┘     └──────────┘     └──────────┘
     │                │                │                │
   Text/@         Fork-exec       llama.cpp         Local
   Voice           No server       Quantized         ONNX


- **Go:** Handles UI, hotkeys, process orchestration
- **Python:** Only for model inference (stateless, dies after each call)
- **Piper:** Local neural TTS, 60MB model, CPU realtime

## Requirements

- Linux x64
- 4GB RAM minimum
- Python 3.8+
- Go 1.20+
- Microphone (for voice input)
- Speakers (for voice output)

## Quick Start

``` bash
git clone <your-repo>
cd "2. Elara simple"
./setup.sh
source venv/bin/activate
./elara
```

## Usage

```bash
> how do I check disk space
← df -h

> @
[VOICE] Recording 5 seconds...
[VOICE] Transcribed: restart nginx
← sudo systemctl restart nginx

> quit
```

## Manual Setup (if setup.sh fails)

```bash
# 1. Python dependencies
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 2. Piper binary
wget https://github.com/rhasspy/piper/releases/download/v1.2.0/piper_amd64.tar.gz
tar -xzf piper_amd64.tar.gz

# 3. Voice model
mkdir -p models
wget https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/lessac/medium/en_US-lessac-medium.onnx -P models/
wget https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/lessac/medium/en_US-lessac-medium.onnx.json -P models/

# 4. System dependencies (Arch)
sudo pacman -S alsa-utils espeak sox

# 5. Build
go build -o elara main.go
```

## System Dependencies

| Package | Purpose | Install |
|---------|---------|---------|
| alsa-utils | Audio playback | `sudo pacman -S alsa-utils` |
| espeak | Fallback TTS | `sudo pacman -S espeak` |
| sox | Audio recording | `sudo pacman -S sox` |

## Project Structure

```
elara/
├── elara              # Compiled binary
├── main.go            # Go entry point
├── setup.sh           # One-command setup
├── requirements.txt   # Python deps
├── model/
│   ├── model.py       # Python inference wrapper
│   └── tier1.py       # LLM engine (llama.cpp)
├── voice/
│   ├── stt.py         # Whisper STT
│   └── tts.py         # Piper TTS wrapper
├── models/            # Downloaded models (gitignored)
└── piper/             # Piper binary + libs (gitignored)
```

## Configuration

Edit `config.yaml` to adjust:
- Model paths
- Voice recording duration
- TTS speed
- CPU threads

## Troubleshooting

**No audio output:**
- Check `aplay -l` for devices
- Ensure `alsa-utils` installed
- Try `espeak "test"` to verify fallback

**STT not working:**
- Check microphone in `arecord -l`
- Install `sox` if `arecord` unavailable

**Model not loading:**
- Download GGUF model to `models/`
- Verify path in `config.yaml`

## License

MIT - Open source, free forever.
