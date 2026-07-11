# config/settings.py
import os
from pathlib import Path
from dotenv import load_dotenv

# 1. Establish the absolute path to your D:/Projects/ARCEUS root directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent
ENV_PATH = PROJECT_ROOT / '.env'

# 2. Load the environment file from the explicit absolute destination
load_dotenv(dotenv_path=ENV_PATH)

# 3. Retrieve and export all keys required by the AI engine
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# 4. Fallback system personality in case it isn't defined in the .env
SYSTEM_PROMPT = os.getenv(
    "SYSTEM_PROMPT",
    "You are ARCEUS, a highly advanced, intelligent desktop AI assistant. "
    "Execute commands efficiently and maintain structural control over the system."
)

# 5. Core peripheral preferences
SPEECH_RATE = int(os.getenv("SPEECH_RATE", 150))

# 6. Safety validation check to catch setup problems early
if not GEMINI_API_KEY and not GROQ_API_KEY:
    raise ValueError(
        f"Initialization Failure: No API keys resolved.\n"
        f"Checked Absolute Path: {ENV_PATH}\n"
        f"Please ensure either GEMINI_API_KEY or GROQ_API_KEY is defined inside your .env file."
    )