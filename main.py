# main.py
import os
import time
from core.audio import AudioInterface
from core.brain import ArceusBrain
from config.settings import WAKE_WORD

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def run_arceus():
    clear_screen()
    print("==================================================")
    print("|| ARCEUS TACTICAL AI - BOOT SEQUENCE COMPLETE  ||")
    print("|| Humor Setting: 75% | Honesty Setting: 90%    ||")
    print("==================================================")

    audio = AudioInterface()
    brain = ArceusBrain()
    
    audio.speak("Systems online. Monitoring for wake word.")

    while True:
        print("[Listening...]", end="\r")
        background_text = audio.listen()
        
        if WAKE_WORD in background_text:
            command = background_text.replace(WAKE_WORD, "").strip()
            
            # If they just called the name, wait for a command
            if not command:
                audio.speak("Awaiting instructions.")
                command = audio.listen(timeout=5, phrase_time=10)
                
            if command:
                print(f"\n[User]: {command}")
                
                # Check for easter eggs first
                if "self destruct" in command:
                    audio.speak("Self-destruct in three. Two. One. Boom. Standard humor setting response.")
                    continue
                    
                # Fetch AI response
                reply = brain.generate_response(command)
                audio.speak(reply)
                
        time.sleep(0.1)

if __name__ == "__main__":
    try:
        run_arceus()
    except KeyboardInterrupt:
        print("\n[ARCEUS]: Manual override accepted. Powering down.")