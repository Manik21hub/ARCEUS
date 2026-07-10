# core/brain.py
import re
from google import genai
from google.genai import types
from config.settings import GEMINI_API_KEY, SYSTEM_PROMPT

class ArceusBrain:
    def __init__(self):
        self.client = genai.Client(api_key=GEMINI_API_KEY)
        self.chat = self.client.chats.create(
            model="gemini-3.1-flash-lite",  # Switched to the high-volume, stable model
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                max_output_tokens=100
            )
        )

    def generate_response(self, user_command):
        try:
            response = self.chat.send_message(user_command)
            clean_text = re.sub(r'[^a-zA-Z0-9\s.,!?\'-]', '', response.text).strip()
            return clean_text
        except Exception as e:
            print(f"\n[API ERROR]: {str(e)}\n")
            return "My circuits are fried. Check the error log."