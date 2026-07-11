# core/brain.py
import re
from google import genai
from groq import Groq
from config.settings import GEMINI_API_KEY, GROQ_API_KEY, SYSTEM_PROMPT
from core.memory import ArceusMemory
from core.features import FeatureManager  # <--- Import the new engine

class ArceusBrain:
    def __init__(self):
        self.memory = ArceusMemory() 
        self.features = FeatureManager()  # <--- Initialize the feature engine
        self.gemini_client = genai.Client(api_key=GEMINI_API_KEY)
        self.groq_client = Groq(api_key=GROQ_API_KEY)
        self.groq_model = "llama-3.3-70b-versatile"
        self.humor_level = 50 
        self.complex_keywords = ["analyze", "research", "strategy", "vulnerability", "drone", "iot", "network", "calculate", "debug", "latest", "news", "current"]

    def _get_dynamic_prompt(self):
        mem_context = self.memory.get_context()
        return (f"{SYSTEM_PROMPT} Current Humor Intensity: {self.humor_level}%. "
                f"System Memory Bank: {mem_context}. "
                "CRITICAL: Do not narrate your actions, do not mention your settings, "
                "do not explain your personality. Be sharp, dry, and answer in 1-3 sentences.")

    def _is_complex(self, text):
        return any(keyword in text.lower() for keyword in self.complex_keywords)

    def generate_response(self, user_command):
        cmd_lower = user_command.lower()

        # 1. Check if this is a predefined Feature (like Music)
        feature_response = self.features.process(cmd_lower)
        if feature_response:
            return feature_response  # If it's a feature, stop here and return the response

        # 2. Memory Storage Command
        if "remember that" in cmd_lower:
            fact = re.split(r'remember that', cmd_lower, maxsplit=1)[1].strip()
            if fact:
                self.memory.add_fact(fact)
                return f"Archived to long-term memory. I shall try not to let it clutter the drives."

        # 3. Humor Calibration Handler
        humor_match = re.search(r'change humor to (\d+)', cmd_lower)
        if humor_match:
            self.humor_level = int(humor_match.group(1))
            return f"Humor level calibrated to {self.humor_level} percent."

        prompt = self._get_dynamic_prompt()

        # 4. Standard LLM Routing (For general conversation and research)
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