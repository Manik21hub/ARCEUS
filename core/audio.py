# core/audio.py
import os
import speech_recognition as sr
from gtts import gTTS
import pygame
import tkinter as tk
import time

class AudioInterface:
    def __init__(self):
        # Initialize pygame mixer for reliable audio playback
        pygame.mixer.init()
        
        self.recognizer = sr.Recognizer()
        print("[System] Calibrating microphone... Please stand by.")
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1.0)
            
        self.recognizer.energy_threshold = 200 
        self.recognizer.non_speaking_duration = 0.4
        self.recognizer.pause_threshold = 0.8  
        
        self.setup_ui()
        print("[System] Calibration complete.")

    def setup_ui(self):
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.attributes("-alpha", 0.7)
        self.root.configure(bg="#000000")
        
        window_width = 150
        window_height = 40
        x = self.root.winfo_screenwidth() - window_width - 20
        y = 20
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        label = tk.Label(
            self.root, 
            text="ARCEUS", 
            fg="#00FF66", 
            bg="#000000", 
            font=("Courier New", 14, "bold")
        )
        label.pack(expand=True, fill="both")
        
        self.root.withdraw()
        self.root.update()

    def speak(self, text):
        print(f"\n[ARCEUS]: {text}\n")
        try:
            # Generate the audio file using Google TTS
            tts = gTTS(text=text, lang='en', tld='co.uk') # Using the UK voice for a slightly more distinguished AI tone
            filename = "response.mp3"
            tts.save(filename)
            
            # Play the audio file reliably
            pygame.mixer.music.load(filename)
            pygame.mixer.music.play()
            
            # Wait for the audio to finish playing
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
                
            # Clean up the audio engine so we can delete the temp file
            pygame.mixer.music.unload()
            os.remove(filename)
            
        except Exception as e:
            print(f"[Audio Error]: {e}")

    def listen(self, timeout=None, phrase_time=None, is_active=False):
        self.root.update()
        with sr.Microphone() as source:
            if is_active:
                self.root.deiconify()
                self.root.update()
                
            try:
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time)
                if is_active:
                    self.root.withdraw()
                    self.root.update()
                return self.recognizer.recognize_google(audio).lower()
            except (sr.WaitTimeoutError, sr.UnknownValueError, sr.RequestError):
                if is_active:
                    self.root.withdraw()
                    self.root.update()
                return ""