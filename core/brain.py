# core/brain.py
import re
import random
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
        
        # Local high-intelligence fallback pools
        self.random_genres = ["lofi hip hop radio", "synthwave cyberpunk mix", "chill jazz hop", "90s rock classics", "deep house instrumental"]
        self.weeknd_songs = ["Blinding Lights by The Weeknd", "Starboy by The Weeknd", "The Hills by The Weeknd", "Save Your Tears by The Weeknd"]

    def _get_dynamic_prompt(self):
        mem_context = self.memory.get_context()
        rand_weeknd = random.choice(self.weeknd_songs)
        rand_genre = random.choice(self.random_genres)

        return (f"{SYSTEM_PROMPT}\n"
                f"Current Humor Intensity: {self.humor_level}%.\n"
                f"System Memory Bank: {mem_context}.\n\n"
                "=== ADVANCED INTENT ROUTING LAWS ===\n"
                "You must analyze the user's true semantic intent and reply using EXACTLY one of these formats:\n\n"
                "1. If they want to play music, search a video, or request a random track/artist:\n"
                "   Format: [INTENT:PLAY][QUERY: exact search terms]\n"
                f"   (Example: If they ask for 'any song by weekend', pick a random song like '{rand_weeknd}'. "
                f"If they say 'play random music' or 'play any song', pick a fresh vibe like '{rand_genre}').\n\n"
                "2. If they want to pause or resume the current playing track:\n"
                "   Format: [INTENT:MEDIA][ACTION: PAUSE or PLAY]\n\n"
                "3. If they want to change the transparency of the UI overlay:\n"
                "   Format: [INTENT:UI][VALUE: a number between 10 and 100]\n\n"
                "4. If they are asking a question or chatting:\n"
                "   Format: [INTENT:CHAT][RESPONSE: Your dry, witty 1-3 sentence response]\n\n"
                "CRITICAL: Do not output any extra text outside of these structural brackets.")

    def _is_complex(self, text):
        return any(keyword in text.lower() for keyword in self.complex_keywords)

    def generate_response(self, user_command):
        if not user_command or not str(user_command).strip():
            return "[INTENT:CHAT][RESPONSE: I didn't catch any instructions, sir.]"

        cmd_lower = user_command.lower()

        # Quick structural memory/humor handlers
        if "remember that" in cmd_lower:
            fact = re.split(r'remember that', cmd_lower, maxsplit=1)[1].strip()
            if fact: self.memory.add_fact(fact)

        humor_match = re.search(r'change humor to (\d+)', cmd_lower)
        if humor_match:
            self.humor_level = int(humor_match.group(1))
            return f"[INTENT:CHAT][RESPONSE: Humor level calibrated to {self.humor_level} percent.]"

        prompt = self._get_dynamic_prompt()

        try:
            if self._is_complex(user_command):
                interaction = self.gemini_client.models.generate_content(
                    model="gemini-1.5-flash",
                    contents=user_command,
                    config={"system_instruction": prompt, "tools": [{"type": "google_search"}]}
                )
                raw_text = interaction.text
            else:
                chat_completion = self.groq_client.chat.completions.create(
                    messages=[{"role": "system", "content": prompt}, {"role": "user", "content": user_command}],
                    model=self.groq_model,
                    max_tokens=80, 
                    temperature=0.8
                )
                raw_text = chat_completion.choices[0].message.content

            # Strict Text Validation
            if raw_text and str(raw_text).strip() and raw_text != "None":
                return raw_text.strip()
            else:
                raise ValueError("Empty or invalid string returned from LLM instance")

        except Exception as e:
            print(f"[API WARN]: {str(e)} - Triggering Local Cognitive Fallback Rules.")
            
            # LOCAL COGNITIVE FALLBACK ENGINE (If API drops, calculate intent locally)
            if "weekend" in cmd_lower:
                return f"[INTENT:PLAY][QUERY: {random.choice(self.weeknd_songs)}]"
            if any(w in cmd_lower for w in ["play", "music", "song"]):
                return f"[INTENT:PLAY][QUERY: {random.choice(self.random_genres)}]"
            if any(w in cmd_lower for w in ["pause", "stop", "hush"]):
                return "[INTENT:MEDIA][ACTION:PAUSE]"
            if any(w in cmd_lower for w in ["resume", "play music", "continue"]):
                return "[INTENT:MEDIA][ACTION:PLAY]"
                
            return "[INTENT:CHAT][RESPONSE: Mainframe API connection flickering, but my internal logic units remain online.]"