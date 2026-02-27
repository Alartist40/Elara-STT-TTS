  **README.md**

```markdown
# Elara Mini

A lightweight, offline IT assistant for old and small devices. 4GB RAM target. No cloud dependencies. Voice-interruptible conversations.

## What It Does

- **Text/Voice Input:** Type normally or press `@` to speak
- **AI Response:** Local LLM (TinyLlama 1.1B) generates answers
- **Voice Output:** Piper TTS speaks the response aloud
- **Interrupt:** Press `@` while speaking to cut off and start new voice input, or type `stop`
- **Use Case:** System administration help without internet or heavy resources

## Architecture

```
┌─────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐
│  User   │────→│  Go Main │────→│  Python  │────→│  Piper   │
│ Input   │     │  Loop    │     │  Model   │     │  TTS     │
└─────────┘     └──────────┘     └──────────┘     └──────────┘
     │                │                │                │
   Text/@         Fork-exec       llama.cpp         Local
   Voice           No server       Quantized         ONNX
   Interrupt       Kill TTS        4 backends        Interruptible
```

- **Go:** Handles UI, hotkeys, process orchestration, TTS kill signals
- **Python:** Only for model inference (stateless, dies after each call)
- **Piper:** Local neural TTS, 60MB model, CPU realtime, killable process
- **Interrupt System:** `@` key kills TTS process tree before recording

## Requirements

- Linux x64
- 4GB RAM minimum
- Python 3.8+
- Go 1.20+
- Microphone (for voice input)
- Speakers (for voice output)

## Quick Start

```bash
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

> explain the kernel  [starts speaking...]
> @                 [cuts off, starts new recording]
[VOICE] Recording 5 seconds...

> stop              [cuts current speech]
[TTS Stopped]

> quit
```

## Commands

| Command | Action |
|---------|--------|
| `quit` | Exit program |
| `stop` | Interrupt current speech |
| `@` | Start voice recording (interrupts if speaking) |
| `@text` | Use "text" as voice input without recording |

## Backend Options

Edit `config.yaml` to switch backends:

```yaml
model:
  backend: "local"  # local | api | ollama | download
```

- **local:** Default, uses downloaded GGUF model
- **api:** OpenAI/Anthropic API (requires `ELARA_API_KEY`)
- **ollama:** Local Ollama instance (requires Ollama running)
- **download:** Auto-download from HuggingFace on first run

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
├── main.go            # Go entry point (interrupt handling)
├── setup.sh           # One-command setup
├── requirements.txt   # Python deps
├── config.yaml        # Backend configuration
├── model/
│   ├── model.py       # Python inference router
│   └── backends/      # 4 backend implementations
│       ├── __init__.py
│       ├── local.py   # llama.cpp backend
│       ├── api.py     # OpenAI/Anthropic API
│       ├── ollama.py  # Ollama HTTP backend
│       └── download.py# HF auto-download
├── voice/
│   ├── stt.py         # Whisper STT
│   └── tts.py         # Piper TTS wrapper
├── models/            # Downloaded models (gitignored)
└── piper/             # Piper binary + libs (gitignored)
```

## Configuration

Edit `config.yaml` to adjust:
- Model backend (local/api/ollama/download)
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

**Interrupt not working:**
- `pkill` must be available (standard on Linux)
- Check no permission issues killing processes

## License

MIT - Open source, free forever.