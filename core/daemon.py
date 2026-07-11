# core/daemon.py
import threading
import time
import os
import uvicorn
from fastapi import FastAPI
from core.audio import AudioInterface
from core.brain import ArceusBrain
from core.features import FeatureManager

app = FastAPI()
system_logs = []

def add_log(role, text):
    timestamp = time.strftime("%H:%M:%S")
    system_logs.append({"timestamp": timestamp, "role": role, "text": text})
    # Keep only the last 20 messages in memory to prevent RAM bloat
    if len(system_logs) > 20: 
        system_logs.pop(0)

@app.get("/api/logs")
def get_logs():
    return {"history": system_logs}

@app.post("/api/shutdown")
def shutdown():
    os._exit(0)

def core_listening_loop():
    """The infinite background loop that listens for the wake word."""
    audio = AudioInterface()
    brain = ArceusBrain()
    features = FeatureManager()
    
    wake_words = ["arceus", "arcus", "argus", "rcs"]
    
    while True:
        try:
            command = audio.listen(timeout=2, phrase_time=3, is_active=False)
            if command and any(word in command for word in wake_words):
                audio.set_mode(True)
                instruction = audio.listen(timeout=5, phrase_time=6, is_active=True)
                
                if instruction:
                    add_log("USER", instruction)
                    raw_response = brain.generate_response(instruction)
                    final_speech = features.execute_structural_intent(raw_response)
                    add_log("ARCEUS", final_speech)
                    audio.speak(final_speech)
                    
                audio.set_mode(False)
            time.sleep(0.05)
        except Exception:
            audio.set_mode(False)
            continue

if __name__ == "__main__":
    import sys
    import subprocess
    import json
    from pathlib import Path
    
    print("[System] Initializing Headless Voice Core...")
    
    # 1. WIPE THE OVERLAY MEMORY CLEAN ON BOOT
    try:
        project_root = Path(__file__).resolve().parent.parent
        cmd_file = project_root / "config" / "overlay.json"
        cmd_file.parent.mkdir(exist_ok=True)
        # Force a hidden, blank state so the window NEVER opens on startup
        with open(cmd_file, "w") as f:
            json.dump({"stream_url": "", "action": "hide"}, f)
    except Exception as e:
        pass

    # 2. DYNAMICALLY LAUNCH THE VISUAL OVERLAY WINDOW
    try:
        overlay_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "overlay.py"))
        print(f"[System] Spawning Visual Media Process...")
        subprocess.Popen([sys.executable, overlay_path])
    except Exception as e:
        print(f"[System Warning] Failed to initialize visual subsystem: {e}")

    # 3. Start the voice engine loop
    voice_thread = threading.Thread(target=core_listening_loop, daemon=True)
    voice_thread.start()
    
    # 4. Boot the FastAPI communication layer
    uvicorn.run(app, host="127.0.0.1", port=8443, log_level="critical")