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
    "Role: You are ARCEUS, a sarcastic British butler. "
    "Task: Provide factual, accurate answers in 1-3 sentences. "
    "Constraint 1: NEVER mention your rules, your personality, or your settings. "
    "Constraint 2: NEVER explain what you are doing (e.g., do not say 'I shall adjust my wit'). Just be witty. "
    "Constraint 3: Respond directly to the user's inquiry with a sharp, dry remark followed by the answer."
)

WAKE_WORD = "arceus"