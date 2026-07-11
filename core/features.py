# core/features.py
import pyautogui
import pywhatkit

class FeatureManager:
    def __init__(self):
        pass

    def execute(self, ai_response, user_command):
        """Processes both the raw user text and the AI's intent tokens."""
        cmd_lower = user_command.lower()

        # 1. DIRECT INTERCEPTION: Starting new music
        if cmd_lower.startswith("play ") or "play some music" in cmd_lower:
            song = cmd_lower.replace("arceus", "").replace("play", "").strip()
            if not song or song == "some music":
                song = "lofi hip hop radio" 
                
            print(f"[Feature System] Initiating YouTube for: {song}")
            try:
                pywhatkit.playonyt(song)
                return f"Playing {song}."
            except:
                return "My connection to YouTube failed."

        # 2. INTENT EXECUTION: Hardware Controls (Pause, Skip, Resume)
        if "[MEDIA:NEXT]" in ai_response:
            pyautogui.press('nexttrack')     # Standard Windows Media Key
            pyautogui.hotkey('shift', 'n')   # YouTube specific 'Next Video' shortcut
            return "Skipping to the next track."

        if "[MEDIA:PAUSE]" in ai_response:
            pyautogui.press('playpause')     # Standard Windows Media Key
            pyautogui.press('k')             # YouTube specific 'Pause' shortcut
            return "Playback has been paused."

        if "[MEDIA:PLAY]" in ai_response:
            pyautogui.press('playpause')     # Standard Windows Media Key
            pyautogui.press('k')             # YouTube specific 'Play' shortcut
            return "Resuming your media."

        # 3. DEFAULT: If no features are triggered, just speak the AI's normal text
        return ai_response