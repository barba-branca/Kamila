import speech_recognition as sr

class STTEngine:
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def listen(self):
        with sr.Microphone() as source:
            print("Diga alguma coisa...")
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)
            try:
                text = self.recognizer.recognize_google(audio, language='pt-BR')
                print(f"Você disse: {text}")
                return text
            except sr.UnknownValueError:
                print("Não foi possível entender o áudio.")
                return None
            except sr.RequestError as e:
                print(f"Erro no serviço de reconhecimento de voz; {e}")
                return None
