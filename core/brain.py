# core/brain.py
import re
from google import genai
from groq import Groq
from config.settings import GEMINI_API_KEY, GROQ_API_KEY, SYSTEM_PROMPT
from core.memory import ArceusMemory

class ArceusBrain:
    def __init__(self):
        self.memory = ArceusMemory() 
        self.gemini_client = genai.Client(api_key=GEMINI_API_KEY)
        self.groq_client = Groq(api_key=GROQ_API_KEY)
        self.groq_model = "llama-3.3-70b-versatile"
        self.humor_level = 50 
        self.complex_keywords = ["analyze", "research", "strategy", "vulnerability", "drone", "iot", "network", "calculate", "debug", "latest", "news", "current"]

    def _get_dynamic_prompt(self):
        mem_context = self.memory.get_context()
        return (f"{SYSTEM_PROMPT} Current Humor Intensity: {self.humor_level}%. "
                f"System Memory Bank: {mem_context}. "
                "\n=== INTENT CONTROLS ===\n"
                "If the user wants to change/skip/stop/pause music or video, you must choose ONE of these tokens and reply ONLY with the token, nothing else:\n"
                "- If they want to skip/change/next track: [MEDIA:NEXT]\n"
                "- If they want to pause/stop/hush: [MEDIA:PAUSE]\n"
                "- If they want to resume/play/continue: [MEDIA:PLAY]\n"
                "If they want you to remember something, save it and reply normally.\n"
                "Otherwise, answer their question directly in 1-3 sentences. Do not explain your settings.")

    def _is_complex(self, text):
        return any(keyword in text.lower() for keyword in self.complex_keywords)

    def generate_response(self, user_command):
        cmd_lower = user_command.lower()

        # Handle explicit humor adjustments fast
        humor_match = re.search(r'change humor to (\d+)', cmd_lower)
        if humor_match:
            self.humor_level = int(humor_match.group(1))
            return f"Humor level calibrated to {self.humor_level} percent."

        prompt = self._get_dynamic_prompt()

        try:
            if self._is_complex(user_command):
                interaction = self.gemini_client.models.generate_content(
                    model="gemini-1.5-flash",
                    contents=user_command,
                    config={
                        "system_instruction": prompt,
                        "tools": [{"type": "google_search"}]
                    }
                )
                raw_text = interaction.text
            else:
                chat_completion = self.groq_client.chat.completions.create(
                    messages=[{"role": "system", "content": prompt}, 
                              {"role": "user", "content": user_command}],
                    model=self.groq_model,
                    max_tokens=60, 
                    temperature=0.7
                )
                raw_text = chat_completion.choices[0].message.content

            # Handle memory updates if the LLM detects a fact mapping
            if "remember that" in cmd_lower:
                fact = re.split(r'remember that', cmd_lower, maxsplit=1)[1].strip()
                if fact:
                    self.memory.add_fact(fact)

            # Return raw string (clean up markdown/emojis)
            return re.sub(r'[^a-zA-Z0-9\s.,!?\'\[\]:]', '', raw_text).strip()

        except Exception as e:
            print(f"\n[API ERROR]: {str(e)}\n")
            return "My circuits are momentarily struggling to process that request."