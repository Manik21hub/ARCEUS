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
        
        return (f"{SYSTEM_PROMPT}\n"
                f"Current Humor Intensity: {self.humor_level}%.\n"
                f"System Memory Bank: {mem_context}.\n\n"
                "=== ADVANCED COGNITIVE ROUTING LAWS ===\n"
                "Analyze the user's semantic intent. If the request requires multiple steps or OS control, "
                "you MUST use the AGENT intent to chain actions together.\n\n"
                "1. INTERNAL MEDIA (Playing specific tracks in your custom holographic overlay):\n"
                "   Format: [INTENT:PLAY][QUERY: exact search terms]\n"
                "   Format: [INTENT:MEDIA][ACTION: PAUSE/PLAY/NEXT/OPACITY_50]\n\n"
                "2. AUTONOMOUS AGENT (PC control, EXTERNAL media like Brave/Spotify, and multi-step tasks):\n"
                "   Format: [THOUGHT: your internal logic] [INTENT:AGENT] [CMD:ACTION|Target]\n"
                "   Available CMD Actions: \n"
                "   - OPEN (e.g., [CMD:OPEN|brave] or [CMD:OPEN|spotify])\n"
                "   - SEARCH (e.g., [CMD:SEARCH|drone topologies])\n"
                "   - TYPE (e.g., [CMD:TYPE|Hello world])\n"
                "   - HOTKEY (e.g., [CMD:HOTKEY|playpause] to pause Brave/Spotify globally!)\n"
                "   - HOTKEY (e.g., [CMD:HOTKEY|nexttrack] or [CMD:HOTKEY|prevtrack])\n"
                "   - HOTKEY (e.g., [CMD:HOTKEY|ctrl+w] to close a tab, or [CMD:HOTKEY|ctrl+t] for new tab)\n"
                "   \n"
                "   EXAMPLES:\n"
                "   User: 'Pause the music in Brave.'\n"
                "   Output: [THOUGHT: The user wants to pause external OS media. I will trigger the global media key.] [INTENT:AGENT] [CMD:HOTKEY|playpause]\n\n"
                "   User: 'Close this tab in Brave.'\n"
                "   Output: [THOUGHT: I need to ensure Brave is focused, then send the close tab hotkey.] [INTENT:AGENT] [CMD:OPEN|brave] [CMD:HOTKEY|ctrl+w]\n\n"
                "3. CHAT (Questions or standard conversation):\n"
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