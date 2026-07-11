# core/features.py
import pywhatkit

class FeatureManager:
    def __init__(self):
        pass

    def process(self, command):
        """Scans the command to see if it matches any installed features."""
        cmd_lower = command.lower()

        # Feature 1: Media Controller
        if cmd_lower.startswith("play ") or "play some music" in cmd_lower:
            return self._play_youtube(cmd_lower)

        # You can easily add Feature 2 (Weather), Feature 3 (Smart Home), etc. here later.

        # If no feature is triggered, return None to let the AI brain handle it.
        return None 

    def _play_youtube(self, command):
        song = command.replace("arceus", "").replace("play", "").strip()
        
        if not song or song == "some music":
            song = "lofi hip hop radio" 

        print(f"[Feature System] Executing YouTube protocol for: {song}")
        
        try:
            pywhatkit.playonyt(song)
            return f"Playing {song}. Try not to let the rhythm distract you from your work."
        except Exception as e:
            print(f"[Feature Error]: {e}")
            return "It seems my connection to YouTube is currently compromised."