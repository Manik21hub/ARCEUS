# main.py
import os
import time
from core.audio import AudioInterface
from core.brain import ArceusBrain

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def run_arceus():
    clear_screen()
    print("==================================================")
    print("|| ARCEUS TACTICAL AI - DIAGNOSTIC MODE ACTIVE  ||")
    print("==================================================")

    audio = AudioInterface()
    brain = ArceusBrain()
    
    audio.speak("Systems online. Monitoring environment.")
    
    # Injected the exact spelling errors your microphone logs generated
    wake_words = ["arceus", "rcs", "are see us", "arkius", "argius", "rcus", "rc", "arc", "rk"]

    while True:
        # Increased phrase_time to 7 seconds to keep the window open longer
        background_text = audio.listen(timeout=2, phrase_time=7, is_active=False)
        
        if background_text:
            print(f"\n[Debug - Heard in Background]: {background_text}")
        
        detected_wake_word = next((word for word in wake_words if word in background_text), None)
        
        if detected_wake_word:
            print(f"[System] Wake word '{detected_wake_word}' triggered!")
            command = background_text.replace(detected_wake_word, "").strip()
            
            if not command:
                audio.speak("Yes?")
                print("[System] Listening for your command...")
                command = audio.listen(timeout=5, phrase_time=10, is_active=True)
                
            if command:
                print(f"[System - User Command Heard]: {command}")
                print("[System] Sending to AI Brain...")
                
                reply = brain.generate_response(command)
                
                print(f"[System - AI Raw Output]: {reply}")
                print("[System] Sending to Voice Engine...")
                
                audio.speak(reply)
                print("[System] Voice Engine finished speaking.")
            else:
                print("[System] No command attached.")
                
        time.sleep(0.1)

if __name__ == "__main__":
    try:
        run_arceus()
    except KeyboardInterrupt:
        print("\n[ARCEUS]: Powering down.")