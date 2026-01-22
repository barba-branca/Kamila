import pytest
from .kamila.core.interpreter import CommandInterpreter

@pytest.fixture
def interpreter():
    return CommandInterpreter()

@pytest.mark.parametrize("command, expected_intent", [
    ("que horas são", "time"),
    ("como você está", "status"),
    ("ligar luz", "lights"),
    ("tocar música", "music"),
    ("comando inexistente", None),
])
def test_interpret_command(interpreter, command, expected_intent):
    intent = interpreter.interpret_command(command)
    assert intent == expected_intent
