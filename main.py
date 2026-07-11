import time
from core.audio import AudioInterface
from core.brain import ArceusBrain

def main():
    audio = AudioInterface()
    brain = ArceusBrain()
    
    # Common ways Google mishears "Arceus"
    wake_words = ["arceus", "arcus", "argus", "rcs", "rc is", "arthur", "arcias"]
    
    print("[System] ARCEUS online. Awaiting verbal trigger.")
    
    while True:
        try:
            # Standby listener
            command = audio.listen(timeout=2, phrase_time=3, is_active=False)
            
            if command:
                # DEBUG: This will show you exactly what Google heard. 
                # If it consistently hears a specific wrong word, add it to the wake_words list above!
                print(f"[Standby Heard]: {command}") 
                
                # Check if ANY of the wake words are in the command
                if any(word in command for word in wake_words):
                    audio.set_mode(True)
                    print("[System] TRIGGERED. Listening for command...")
                    
                    instruction = audio.listen(timeout=5, phrase_time=6, is_active=True)
                    
                    if instruction and len(instruction) > 2:
                        print(f"[User]: {instruction}")
                        response = brain.generate_response(instruction)
                        audio.speak(response)
                    else:
                        print("[System] Command aborted or unclear.")
                    
                    audio.set_mode(False)
            
            time.sleep(0.05)
            
        except Exception as e:
            audio.set_mode(False)
            continue

if __name__ == "__main__":
    main()