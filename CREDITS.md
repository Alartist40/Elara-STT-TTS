# Credits

## Core Dependencies

- **[Piper](https://github.com/rhasspy/piper)** - Fast, local neural text-to-speech by Rhasspy
- **[OpenAI Whisper](https://github.com/openai/whisper)** - Speech recognition model
- **[llama-cpp-python](https://github.com/abetlen/llama-cpp-python)** - Python bindings for llama.cpp
- **[Go](https://golang.org/)** - Systems programming language for the main loop
- **[readline](https://github.com/chzyer/readline)** - Go library for terminal input handling

## Architecture Inspiration

- **[PersonaPlex/Moshi](https://github.com/nvidia/personaplex)** - NVIDIA's full-duplex conversational AI. Interrupt handling pattern adapted from their async WebSocket implementation.

## Model Weights

- **[TinyLlama](https://huggingface.co/TinyLlama)** - The TinyLlama project for the base language model
- **[Piper Voices](https://huggingface.co/rhasspy/piper-voices)** - Voice models for TTS

## Tools

- **[HuggingFace](https://huggingface.co/)** - Model hosting and downloads
- **[Ollama](https://ollama.ai/)** - Local LLM serving (optional backend)

## Special Thanks

- Rhasspy team for Piper TTS
- Georgi Gerganov for llama.cpp
- OpenAI for Whisper
- Kyutai for Moshi architecture patterns

All code used respects their respective licenses (MIT, Apache 2.0, etc).