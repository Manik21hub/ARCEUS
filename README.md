# ARCEUS - humourus human like AI Assistant

ARCEUS is an advanced, highly articulate voice assistant built with a sophisticated, sharply sarcastic British Butler persona. Inspired by cinematic sidekicks, ARCEUS balances a dry, aristocratic wit with flawless factual accuracy—making it a formidable companion for highly complex research domains, such as modern military IoT and drone network analysis.

## 🚀 Features
- **Personality Engine:** A refined British Butler archetype that provides elegant, concise, and mildly condescending humor without compromising factual accuracy.
- **Neural Voice Integration:** Powered by the open-source **Kokoro-82M** engine running entirely locally, utilizing the deeply expressive `bm_george` voice profile.
- **Low Latency Pipeline:** Audio generation is chunked and streamed instantly via `sounddevice`, bypassing heavy cloud API costs or multi-second inference lags.
- **Dynamic HUD UI:** A clean, minimal, translucent floating heads-up display built natively via Tkinter.

## 🛠️ System Architecture
- **Core Brain:** Google Gemini API (via custom system prompts enforcing brevity, accuracy, and wit).
- **Audio Synthesis:** Kokoro TTS (82M Parameter Transformer model).
- **Speech Recognition:** Google Speech Recognition API via `speech_recognition`.
- **UI & Playback:** Tkinter (Heads-Up Display) and Sounddevice (Real-time audio streaming).

## 📦 Installation & Setup

### 1. System Dependencies (Required for Audio Engine)
The local neural phonetic engine requires `espeak-ng` installed on your host OS:
- **Windows:** Download and run the [.msi installer from espeak-ng GitHub](https://github.com/espeak-ng/espeak-ng/releases).
- **macOS:** `brew install espeak`
- **Linux:** `sudo apt-get install espeak-ng`

### 2. Python Environment Setup
Clone the repository and install the tracked dependencies:
```bash
pip install -r requirements.txt