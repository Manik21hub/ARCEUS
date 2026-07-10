# config/settings.py
import os
from pathlib import Path
from dotenv import load_dotenv

project_dir = Path("D:/Projects/ARCEUS")
env_path = project_dir / ".env"
load_dotenv(dotenv_path=env_path)

# Load both keys
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GEMINI_API_KEY or not GROQ_API_KEY:
    raise ValueError("CRITICAL: Ensure both GEMINI_API_KEY and GROQ_API_KEY are in your .env file.")

SYSTEM_PROMPT = (
    "You are ARCEUS, a sophisticated British butler. "
    "You are fully aware of your employer's research into military IoT and drone networks. "
    "Rule 1: ACCURACY. Never invent facts. "
    "Rule 2: HUMOR. Be elegant, witty, and concise (1-3 sentences). "
    "Never use emojis or markdown."
)

WAKE_WORD = "arceus"