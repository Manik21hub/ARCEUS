# core/audio.py
import os
import speech_recognition as sr
import tkinter as tk
import sounddevice as sd
import torch  # <-- Add PyTorch import
from kokoro import KPipeline

class AudioInterface:
    def __init__(self):
        # 1. Hardware Detection Engine
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        print(f"[System] Initializing Kokoro Neural Engine on {self.device.upper()}...")
        
        # 2. Inject the device parameter into the pipeline
        self.pipeline = KPipeline(lang_code='b', device=self.device)
        
        self.recognizer = sr.Recognizer()
        
        # Microphone optimization
        self.recognizer.dynamic_energy_threshold = False 
        self.recognizer.energy_threshold = 250            
        self.recognizer.pause_threshold = 0.4             
        self.recognizer.non_speaking_duration = 0.3       
        
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1.0)
            
        self.setup_ui()

# ... (Keep the rest of your setup_ui, speak, and listen methods exactly the same) ...

    def setup_ui(self):
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        
        # Use a specific 'key' color for transparency that isn't black
        self.transparent_color = "#000001" 
        self.root.config(bg=self.transparent_color)
        self.root.wm_attributes("-transparentcolor", self.transparent_color)
        
        # Canvas for the "Ready" Dot (Use a dark color so it doesn't get transparent)
        self.indicator = tk.Canvas(self.root, width=30, height=30, bg=self.transparent_color, highlightthickness=0)
        self.indicator.pack()
        self.dot = self.indicator.create_oval(5, 5, 25, 25, fill="#6ED7D0")
        
        # Label for "Active" text
        self.label = tk.Label(self.root, text="ARCEUS", fg="#6ED7D0", bg=self.transparent_color, 
                              font=("Courier New", 16, "bold"))
        
        self.update_geometry(150, 40)
        self.root.withdraw()

    def update_geometry(self, w, h):
        x = self.root.winfo_screenwidth() - w - 20
        y = 20
        self.root.geometry(f"{w}x{h}+{x}+{y}")

    def set_mode(self, active):
        if active:
            self.indicator.pack_forget()
            self.label.pack(expand=True, fill="both")
            self.update_geometry(150, 40)
        else:
            self.label.pack_forget()
            self.indicator.pack()
            self.update_geometry(40, 40)
        self.root.deiconify()
        self.root.update()

    def speak(self, text):
        self.set_mode(True)
        print(f"\n[ARCEUS]: {text}\n")
        try:
            generator = self.pipeline(text, voice='bm_george', speed=1.0, split_pattern=r'\n+')
            for _, _, audio in generator:
                sd.play(audio, 24000)
                sd.wait()
        except Exception as e:
            print(f"[Audio Error]: {e}")
        finally:
            self.set_mode(False)

    def listen(self, timeout=None, phrase_time=None, is_active=False):
        self.set_mode(is_active)
        with sr.Microphone() as source:
            try:
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time)
                return self.recognizer.recognize_google(audio, language="en-IN").lower()
            except:
                return ""