 #!/usr/bin/env python3
"""
Teste simples do Command Interpreter
"""

import sys
import os
sys.path.append('.kamila')

from core.interpreter import CommandInterpreter

def test_interpreter():
    print("🧠 Testando Command Interpreter...")

    # Inicializar interpreter
    interpreter = CommandInterpreter()

    # Testar comandos
    commands = [
        'que horas são',
        'como você está',
        'ligar luz',
        'tocar música',
        'comando inexistente'
    ]

    print("\n📝 Resultados:")
    for cmd in commands:
        intent = interpreter.interpret_command(cmd)
        print(f'Comando: "{cmd}" → Intenção: {intent}')

    print("\n✅ Teste concluído!")

if __name__ == "__main__":
    test_interpreter()
