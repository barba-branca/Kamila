import pyttsx3
import logging

logging.basicConfig(level=logging.INFO)

try:
    print("--- INICIANDO TESTE DE ÁUDIO DIRETO ---")
    
    # 1. Tenta inicializar o motor de voz
    print("Passo 1: Inicializando motor de voz...")
    engine = pyttsx3.init()
    print("Motor de voz inicializado.")

    # 2. Lista as vozes disponíveis para diagnóstico
    print("\nPasso 2: Verificando vozes instaladas no seu Windows...")
    voices = engine.getProperty('voices')
    if not voices:
        print("!!! ALERTA: Nenhuma voz encontrada no sistema! Este é o problema. !!!")
    else:
        for i, voice in enumerate(voices):
            print(f"  - Voz {i}: ID={voice.id}")
            # Tenta encontrar e selecionar a voz em Português
            if 'brazil' in voice.name.lower():
                engine.setProperty('voice', voice.id)
                print(f"    --> Selecionada a voz em Português (Brazil): {voice.name}")

    # 3. Configura propriedades
    print("\nPasso 3: Configurando volume e velocidade...")
    engine.setProperty('rate', 180)
    engine.setProperty('volume', 1.0) # Volume máximo para o teste
    print("Propriedades configuradas.")

    # 4. Tenta falar
    text_to_speak = "Se você está ouvindo isso, o sistema de som está funcionando corretamente."
    print(f"\nPasso 4: Tentando falar a frase: '{text_to_speak}'")
    engine.say(text_to_speak)
    
    print("\nPasso 5: Executando .runAndWait()... Se travar aqui, o problema é no driver de áudio.")
    engine.runAndWait() # Este é o comando que realmente produz o som.

    print("\nPasso 6: .runAndWait() concluído com sucesso.")
    print("\n--- TESTE FINALIZADO ---")
    
    if voices:
        print("\n✅ O teste foi concluído sem erros. Você deveria ter ouvido a frase.")
        print("Se você não ouviu, verifique:")
        print("  - O volume do seu computador e dos seus alto-falantes/fones.")
        print("  - Se a saída de áudio padrão do Windows está correta (ex: 'Alto-falantes' e não um monitor HDMI sem som).")
    
except Exception as e:
    print(f"\n--- ERRO CRÍTICO NO TESTE DE ÁUDIO ---")
    print(f"O teste falhou com o seguinte erro: {e}")
    import traceback
    traceback.print_exc()