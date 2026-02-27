# Changelog

## [0.1.0] - 2026-02-27

### Added
- Initial working prototype with full voice pipeline
- `setup.sh` for one-command installation with Go build step
- README.md with full documentation
- Venv Python auto-detection in Go binary with system fallback

### Fixed

#### TTS Implementation
- **Problem:** Piper binary missing shared libraries (`libpiper_phonemize.so.1`)
- **Solution:** Extracted full piper archive including `lib*.so` files to `/usr/local/lib/`, ran `ldconfig`
- **Problem:** `tts.py` using hardcoded model path that didn't exist
- **Solution:** Updated path to `models/en_US-lessac-medium.onnx` using `os.path.join()`

#### Piper Integration
- **Problem:** `tts.py` looked for system `piper` binary only
- **Solution:** Modified to check for local `./piper/piper` binary first, then fall back to system path
- **Problem:** Relative path resolution failed when running from different directories
- **Solution:** Used `os.path.dirname(os.path.abspath(__file__))` to get script location, then traverse to project root

#### Audio Pipeline
- **Problem:** No audio players found on system
- **Solution:** Documented `alsa-utils` requirement, added fallback chain: aplay → paplay → ffplay → afplay
- **Problem:** Static sound only from Piper
- **Solution:** Proper library linking via `ldconfig` after copying `.so` files

#### Build & Distribution
- **Problem:** `setup.sh` not executable on fresh clone
- **Solution:** Added `chmod +x setup.sh` instruction (or user runs `bash setup.sh`)
- **Problem:** `main.go` used system `python3` only, failed if venv not activated
- **Solution:** Added venv detection: checks `./venv/bin/python3` exists, falls back to `python3`
- **Problem:** `setup.sh` missing Go check and build step
- **Solution:** Added Go version check and `go build -o elara main.go` at end
- **Problem:** `llama-cpp-python` install fails without build tools
- **Solution:** Documented `gcc` and `python-dev` requirements in comments

### Changed
- `tts.py` now uses local Piper binary with automatic fallback to espeak
- Model path resolution now relative to script location, not CWD
- `requirements.txt` updated with build tool documentation
- `main.go` all Python calls now use dynamic path resolution (venv → system)
- `setup.sh` now validates Go installation before proceeding

### Architecture Decisions
- **Go + Python split:** Go handles orchestration (fast, no deps), Python handles ML (isolated, dies after inference)
- **Fork-exec model:** No persistent Python processes, memory clears after each query
- **Piper over espeak:** Neural TTS quality for production, espeak fallback for compatibility
- **Local binary distribution:** Piper included in repo structure, not system-installed
- **Venv-first approach:** Prioritize isolated Python environment, fallback to system for flexibility

### Dependencies Added
- Piper 1.2.0 binary (amd64)
- en_US-lessac-medium voice model (60MB)
- espeak-ng libraries (via Piper archive)

### Known Issues
- First-time Piper load takes ~0.3s (acceptable)
- Context warning: `n_ctx_per_seq (4096) &gt; n_ctx_train (2048)` - non-critical, model works fine
- No Windows/Mac support yet (Piper binaries available, paths need adjustment)
- Model file `tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf` must be downloaded manually (not in setup.sh)

### Next Steps
- Add config hot-reload
- Add conversation history
- Optimize model loading (currently loads each time)
- Add more voice models

### Added (v0.2.0)
- **Voice Interrupt System:** Press `@` during speech to immediately cut off TTS and start new recording
- **Stop Command:** Type `stop` to interrupt current speech without new input
- **Process Kill Architecture:** TTS runs as trackable process, killable via `killTTS()` function
- **Backend System:** 4 pluggable backends (local, api, ollama, download) via config.yaml
- **Multi-backend Support:** OpenAI API, Ollama local, HF download, local GGUF

### Changed
- `main.go` now manages TTS process lifecycle with global `currentTTS` variable
- `speak()` kills previous TTS before starting new one
- `voiceInput()` calls `killTTS()` at entry to ensure clean interrupt
- Model loading moved to backend factory pattern

### Technical Details
- Added `killTTS()` function using `Process.Kill()` and `pkill` cleanup
- TTS goroutine now assigns to global variable for tracking
- Added cleanup for aplay/paplay/ffplay/afplay orphans