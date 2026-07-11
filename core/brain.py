# core/brain.py
import re
from google import genai
from groq import Groq
from config.settings import GEMINI_API_KEY, GROQ_API_KEY, SYSTEM_PROMPT
from core.memory import ArceusMemory

class ArceusBrain:
    def __init__(self):
        self.memory = ArceusMemory() # Initialize the memory drive
        self.gemini_client = genai.Client(api_key=GEMINI_API_KEY)
        self.groq_client = Groq(api_key=GROQ_API_KEY)
        self.groq_model = "llama-3.3-70b-versatile"
        self.humor_level = 50 
        self.complex_keywords = ["analyze", "research", "strategy", "vulnerability", "drone", "iot", "network", "calculate", "debug", "latest", "news", "current"]

    def _get_dynamic_prompt(self):
        """Constructs the prompt with humor level, strict brevity, AND long-term memory."""
        mem_context = self.memory.get_context()
        return (f"{SYSTEM_PROMPT} Current Humor Intensity: {self.humor_level}%. "
                f"System Memory Bank: {mem_context}. "
                "CRITICAL: Do not narrate your actions, do not mention your settings, "
                "do not explain your personality. Be sharp, dry, and answer in 1-3 sentences.")

    def _is_complex(self, text):
        return any(keyword in text.lower() for keyword in self.complex_keywords)

    def generate_response(self, user_command):
        # 1. Memory Storage Command ("Arceus, remember that...")
        if "remember that" in user_command.lower():
            # Extract whatever is said after "remember that"
            fact = re.split(r'remember that', user_command.lower(), maxsplit=1)[1].strip()
            if fact:
                self.memory.add_fact(fact)
                return f"Archived to long-term memory. I shall try not to let it clutter the drives."

        # 2. Humor Calibration Handler
        humor_match = re.search(r'change humor to (\d+)', user_command.lower())
        if humor_match:
            self.humor_level = int(humor_match.group(1))
            return f"Humor level calibrated to {self.humor_level} percent."

        prompt = self._get_dynamic_prompt()

        try:
            if self._is_complex(user_command):
                print("[Router] Routing to Gemini (Complex/Search Enabled)")
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
                print("[Router] Routing to Groq (High-Speed)")
                chat_completion = self.groq_client.chat.completions.create(
                    messages=[{"role": "system", "content": prompt}, 
                              {"role": "user", "content": user_command}],
                    model=self.groq_model,
                    max_tokens=60, 
                    temperature=0.7
                )
                raw_text = chat_completion.choices[0].message.content

            clean_text = re.sub(r'[^a-zA-Z0-9\s.,!?\'-]', '', raw_text).strip()
            sentences = re.split(r'(?<=[.!?]) +', clean_text)
            return " ".join(sentences[:3])

        except Exception as e:
            print(f"\n[API ERROR]: {str(e)}\n")
            return "My circuits are momentarily struggling to process that request."