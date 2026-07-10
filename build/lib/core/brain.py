# core/brain.py
import google.generativeai as genai
from config.settings import GEMINI_API_KEY, SYSTEM_PROMPT

class ArceusBrain:
    def __init__(self):
        genai.configure(api_key=GEMINI_API_KEY)
        # Using flash for fast response times suitable for voice
        self.model = genai.GenerativeModel(
            'gemini-1.5-flash',
            system_instruction=SYSTEM_PROMPT
        )
        self.chat = self.model.start_chat(history=[])

    def generate_response(self, user_command):
        try:
            response = self.chat.send_message(user_command)
            # Clean up asterisks or markdown that text-to-speech struggles with
            clean_text = response.text.replace("*", "").strip()
            return clean_text
        except Exception as e:
            return "My communication relays are down. Unable to reach the server."