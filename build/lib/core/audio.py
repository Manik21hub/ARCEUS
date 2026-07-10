# core/audio.py
import speech_recognition as sr
import pyttsx3
from config.settings import SPEECH_RATE

class AudioInterface:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.setup_voice()
        self.recognizer = sr.Recognizer()

    def setup_voice(self):
        voices = self.engine.getProperty('voices')
        # Hunt for a deeper, male voice
        for voice in voices:
            if "male" in voice.name.lower() or "david" in voice.name.lower():
                self.engine.setProperty('voice', voice.id)
                break
        self.engine.setProperty('rate', SPEECH_RATE)

    def speak(self, text):
        print(f"\n[ARCEUS]: {text}\n")
        self.engine.say(text)
        self.engine.runAndWait()

    def listen(self, timeout=2, phrase_time=5):
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            try:
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time)
                return self.recognizer.recognize_google(audio).lower()
            except (sr.WaitTimeoutError, sr.UnknownValueError):
                return ""
            except sr.RequestError:
                print("[Error] Offline.")
                return ""