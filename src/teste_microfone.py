import speech_recognition as sr

r = sr.Recognizer()
with sr.Microphone() as source:
    print("Ajustando para o ruído...")
    r.adjust_for_ambient_noise(source)
    print("Diga alguma coisa!")
    try:
        audio = r.listen(source, timeout=7)
        print("Reconhecendo...")
        texto = r.recognize_google(audio, language='pt-BR')
        print("Você disse: " + texto)
    except sr.UnknownValueError:
        print("Google não conseguiu entender o áudio")
    except sr.RequestError as e:
        print(f"Erro no serviço do Google; {e}")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
