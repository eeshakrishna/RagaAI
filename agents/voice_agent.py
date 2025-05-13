import speech_recognition as sr
import pyttsx3  # For text-to-speech (offline mode)

class VoiceAgent:
    def __init__(self, tts_mode="offline"):
        # Initialize the recognizer for speech-to-text
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

        # Initialize text-to-speech engine (offline)
        self.tts_mode = tts_mode
        if self.tts_mode == "offline":
            self.engine = pyttsx3.init()

    def record_audio(self, duration=5):
        """ Record audio from the microphone for a given duration. """
        with self.microphone as source:
            print("🎤 Listening...")
            self.recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
            audio = self.recognizer.listen(source, phrase_time_limit=duration)
            print("✅ Audio recorded")
        return audio

    def transcribe_audio(self, audio):
        """ Convert the recorded audio to text. """
        try:
            print("📝 Transcribing...")
            text = self.recognizer.recognize_google(audio)  # Use Google STT API
            print(f"📝 Transcribed: {text}")
            return text
        except sr.UnknownValueError:
            print("❌ Could not understand the audio")
            return ""
        except sr.RequestError as e:
            print(f"❌ Could not request results from Google Speech Recognition service; {e}")
            return ""

    def get_transcription(self, duration=5):
        """ Record and transcribe audio. """
        audio = self.record_audio(duration)
        return self.transcribe_audio(audio)

    def speak_text(self, text):
        """ Convert text to speech. """
        print(f"🔊 Speaking: {text}")
        if self.tts_mode == "offline":
            self.engine.say(text)
            self.engine.runAndWait()
        else:
            print("Text-to-speech not available in this mode.")


