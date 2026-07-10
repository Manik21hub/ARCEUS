import re
from google import genai
from google.genai import types
from groq import Groq
from config.settings import GEMINI_API_KEY, GROQ_API_KEY, SYSTEM_PROMPT

class ArceusBrain:
    def __init__(self):
        self.humor_level = 50  # Default humor level (0-100)
        self.gemini_client = genai.Client(api_key=GEMINI_API_KEY)
        self.groq_client = Groq(api_key=GROQ_API_KEY)
        self.groq_model = "llama-3.3-70b-versatile"
        self.complex_keywords = ["analyze", "research", "strategy", "vulnerability", "drone", "iot", "network", "calculate", "debug"]
        
    def _get_system_prompt(self):
        """Generates the prompt dynamically based on the current humor setting."""
        return (f"{SYSTEM_PROMPT} "
                f"Your current humor intensity level is {self.humor_level} percent. "
                f"At this level, balance your Butler persona with the appropriate amount of wit. "
                f"If the level is low, be professional and dry. If high, be extremely sarcastic and roast the user.")

    def generate_response(self, user_command):
        # Check for humor adjustment command
        humor_match = re.search(r'change humor to (\d+)', user_command.lower())
        if humor_match:
            self.humor_level = int(humor_match.group(1))
            return f"Humor level calibrated to {self.humor_level} percent. I shall endeavor to be as amusing or as insufferable as you require."

        try:
            prompt = self._get_system_prompt()
            
            if any(k in user_command.lower() for k in self.complex_keywords):
                # Gemini path
                chat = self.gemini_client.chats.create(
                    model="gemini-1.5-flash", 
                    config=types.GenerateContentConfig(system_instruction=prompt)
                )
                raw_text = chat.send_message(user_command).text
            else:
                # Groq path
                chat = self.groq_client.chat.completions.create(
                    messages=[{"role": "system", "content": prompt}, {"role": "user", "content": user_command}],
                    model=self.groq_model,
                    max_tokens=100
                )
                raw_text = chat.choices[0].message.content

            return re.sub(r'[^a-zA-Z0-9\s.,!?\'-]', '', raw_text).strip()

        except Exception as e:
            return "I apologize, but my circuits are momentarily struggling to process that request."