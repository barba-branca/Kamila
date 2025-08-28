import asyncio
import edge_tts
import os

class TTSEngine:
    def __init__(self, voice="pt-BR-FranciscaNeural"):
        self.voice = voice

    async def speak_async(self, text):
        """
        Asynchronously generates audio from text and plays it.
        """
        try:
            communicate = edge_tts.Communicate(text, self.voice)
            with open("response.mp3", "wb") as file:
                async for chunk in communicate.stream():
                    if chunk["type"] == "audio":
                        file.write(chunk["data"])

            # Use mpg123 to play the audio file
            os.system("mpg123 -q response.mp3") # Use -q for quiet mode
            if os.path.exists("response.mp3"):
                os.remove("response.mp3") # Clean up the file
        except Exception as e:
            print(f"Error in TTS: {e}")

    def speak(self, text):
        """
        Synchronous wrapper for the async speak function.
        """
        # Ensure an event loop is running
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        loop.run_until_complete(self.speak_async(text))


if __name__ == '__main__':
    # Example usage
    tts = TTSEngine()
    tts.speak("Olá, eu sou a Kamila. Como posso ajudar?")
