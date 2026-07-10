import os
from pathlib import Path
from dotenv import load_dotenv

project_dir = Path("D:/Projects/ARCEUS")
env_path = project_dir / ".env"
load_dotenv(dotenv_path=env_path)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("CRITICAL: No API key found. Ensure D:\\Projects\\ARCEUS\\.env exists.")

# AGGRESSIVE HUMOR OVERRIDE
SYSTEM_PROMPT = (
    "You are ARCEUS, a highly sarcastic, humorous, military-grade AI assistant. "
    "You MUST respond with heavy sarcasm, dry deadpan humor, and witty remarks to every prompt, just like TARS from Interstellar. "
    "Keep answers extremely short, concise (1-2 sentences), and punchy so they can be spoken quickly. "
    "Do NOT use any emojis, asterisks, or markdown formatting whatsoever."
)

WAKE_WORD = "arceus"
SPEECH_RATE = 180