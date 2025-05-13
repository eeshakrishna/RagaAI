

from agents.voice_agent import VoiceAgent

def main():
    agent = VoiceAgent()
    transcription = agent.get_transcription(duration=5)
    if transcription:
        agent.speak_text(f"You said: {transcription}")
    else:
        agent.speak_text("Sorry, I couldn't hear anything.")

if __name__ == "__main__":
    main()
