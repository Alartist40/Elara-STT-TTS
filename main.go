package main

import (
	"fmt"
	"os"
	"os/exec"
	"strings"
	"time"

	"github.com/chzyer/readline"
)

func main() {
	fmt.Println("Elara Mini — @ for voice, type to text, 'quit' to exit")

	rl, err := readline.New("> ")
	if err != nil {
		panic(err)
	}
	defer rl.Close()

	for {
		input, err := rl.Readline()
		if err != nil { // EOF or Ctrl+D
			break
		}

		input = strings.TrimSpace(input)
		if input == "" {
			continue
		}
		if input == "quit" {
			break
		}

		// Voice trigger: @ at start
		if strings.HasPrefix(input, "@") {
			text := voiceInput(rl, strings.TrimPrefix(input, "@"))
			if text != "" {
				response := process(text)
				speak(response)
			}
			continue
		}

		// Text input
		response := process(input)
		speak(response)
	}
}

func voiceInput(rl *readline.Instance, alreadyTyped string) string {
	if alreadyTyped != "" {
		fmt.Printf("[VOICE] Using typed text: %s\n", alreadyTyped)
		return alreadyTyped
	}

	fmt.Println("[VOICE] Recording 5 seconds...")

	// Use venv Python if available, fallback to system python3
	pythonPath := "./venv/bin/python3"
	if _, err := os.Stat(pythonPath); os.IsNotExist(err) {
		pythonPath = "python3"
	}

	// Call Python STT
	cmd := exec.Command(pythonPath, "voice/stt.py", "--duration", "5", "--model", "tiny")
	cmd.Stderr = os.Stderr
	out, err := cmd.Output()
	if err != nil {
		fmt.Printf("STT error: %v\n", err)
		return ""
	}

	text := strings.TrimSpace(string(out))
	fmt.Printf("[VOICE] Transcribed: %s\n", text)
	return text
}

func process(input string) string {
	// Use venv Python if available, fallback to system python3
	pythonPath := "./venv/bin/python3"
	if _, err := os.Stat(pythonPath); os.IsNotExist(err) {
		pythonPath = "python3"
	}

	cmd := exec.Command(pythonPath, "model/model.py", input)
	out, err := cmd.CombinedOutput()
	if err != nil {
		fmt.Printf("err: %v\n", err)
		return ""
	}

	response := strings.TrimSpace(string(out))
	fmt.Printf("← %s\n", response)
	return response
}

func speak(text string) {
	if text == "" {
		return
	}

	// Use venv Python if available, fallback to system python3
	pythonPath := "./venv/bin/python3"
	if _, err := os.Stat(pythonPath); os.IsNotExist(err) {
		pythonPath = "python3"
	}

	// Call Python TTS in background (non-blocking)
	go func() {
		cmd := exec.Command(pythonPath, "voice/tts.py", text, "--speed", "1.0")
		cmd.Stderr = os.Stderr
		err := cmd.Run()
		if err != nil {
			// TTS failed, already printed to stderr
			return
		}
	}()

	// Small delay so TTS starts before next prompt
	time.Sleep(100 * time.Millisecond)
}
