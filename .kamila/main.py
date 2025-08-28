from core.stt_engine import STTEngine
from core.tts_engine import TTSEngine
from core.interpreter import Interpreter
from core.actions import Actions
import time

class Kamila:
    def __init__(self):
        self.stt = STTEngine()
        self.tts = TTSEngine()
        self.interpreter = Interpreter()
        self.actions = Actions(self.tts)
        self.state = "IDLE"
        self.context = {}

    def run(self):
        self.tts.speak("Kamila iniciada. Como posso ajudar?")
        while True:
            text = self.stt.listen()
            if not text:
                time.sleep(1)
                continue

            if self.state == "IDLE":
                self.handle_idle_state(text)
            else:
                self.handle_conversation_state(text)

    def handle_idle_state(self, text):
        intent_data = self.interpreter.get_intent(text)
        self.state, self.context = self.actions.execute(intent_data, self.context)

    def handle_conversation_state(self, text):
        # This is a state handler that needs to be expanded.
        # For now, it only handles a simple reservation flow.

        if self.state == "AWAITING_AREA_NAME":
            self.context['area_name'] = text
            response = f"E para qual data você gostaria de reservar a área {self.context['area_name']}?"
            self.tts.speak(response)
            self.state = "AWAITING_RESERVATION_DATE"

        elif self.state == "AWAITING_RESERVATION_DATE":
            self.context['reservation_date'] = text
            area = self.context.get('area_name', 'a área')
            date = self.context.get('reservation_date', 'a data solicitada')
            response = f"Ok, reservei {area} para {date}. Deseja mais alguma coisa?"
            self.tts.speak(response)
            self.state = "IDLE"
            self.context = {} # Reset context

        elif self.state == "AWAITING_CONFIRMATION":
            if "sim" in text.lower():
                action = self.context.get('pending_action', '')
                if action == 'send_boleto':
                    response = "Confirmado. O boleto foi enviado para o seu e-mail."
                elif action == 'commercial_lead':
                    response = "Ótimo! Um de nossos consultores entrará em contato."
                else:
                    response = "Confirmado."
            else:
                response = "Ok, cancelado."

            self.tts.speak(response)
            self.state = "IDLE"
            self.context = {}

        else:
            # Generic handler for other states for now
            self.context['last_input'] = text
            response = f"Anotado: {text}. Processo finalizado. Posso ajudar em algo mais?"
            self.tts.speak(response)
            self.state = "IDLE"
            self.context = {}


if __name__ == "__main__":
    kamila_app = Kamila()
    kamila_app.run()
