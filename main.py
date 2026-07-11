import time
from core.audio import AudioInterface
from core.brain import ArceusBrain
from core.features import FeatureManager

def main():
    audio = AudioInterface()
    brain = ArceusBrain()
    features = FeatureManager()
    
    wake_words = ["arceus", "arcus", "argus", "rcs", "rc is", "arthur", "arcias", "rts"]
    
    print("[System] ARCEUS online. Awaiting verbal trigger.")
    
    while True:
        try:
            # Slightly longer timeout prevents the mic from turning on/off too fast and missing words
            command = audio.listen(timeout=2, phrase_time=3, is_active=False)
            
            if command:
                print(f"[Standby Heard]: {command}") 
                
                if any(word in command for word in wake_words):
                    audio.set_mode(True)
                    print("[System] TRIGGERED. Listening for command...")
                    
                    instruction = audio.listen(timeout=5, phrase_time=6, is_active=True)
                    
                    if instruction and len(instruction) > 2:
                        print(f"[User]: {instruction}")
                        
                        # 1. Ask the AI Brain for a response/token
                        raw_response = brain.generate_response(instruction)
                        
                        # 2. Pass BOTH the AI response and user's original words to the feature engine
                        final_speech = features.execute(raw_response, instruction)
                        
                        # 3. Speak the result
                        audio.speak(final_speech)
                    else:
                        print("[System] Command aborted.")
                    
                    audio.set_mode(False)
            
            time.sleep(0.05)
            
        except Exception as e:
            audio.set_mode(False)
            continue

if __name__ == "__main__":
    main()