# ARCEUS: Tactical Background Voice Assistant

ARCEUS is a military-grade, offline-wake-word AI assistant modeled after TARS from *Interstellar*. It runs seamlessly in the background, listening passively with minimal CPU footprint until called upon. Once activated, it leverages Google's Generative AI to provide concise, practical, and highly sarcastic responses.

## Features
* **Passive Background Listening:** Uses `SpeechRecognition` to monitor audio without actively recording or processing until the wake word ("Arceus") is detected.
* **TARS Personality Engine:** Engineered system prompts enforce a strict 75% humor / 90% honesty threshold, resulting in dry, deadpan, and deeply loyal interactions.
* **Modular Architecture:** Cleanly separated audio processing, AI logic, and configuration for easy scaling or swapping of LLM providers.
* **Offline Text-to-Speech:** Uses `pyttsx3` for zero-latency, robotic voice synthesis.

## Installation & Setup

1. **Clone and enter the repository:**
   ```bash
   git clone [https://github.com/yourusername/arceus-assistant.git](https://github.com/yourusername/arceus-assistant.git)
   cd arceus-assistant