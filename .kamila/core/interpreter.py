import google.generativeai as genai
import os

class Interpreter:
    def __init__(self):
        # Configure the generative AI model
        try:
            genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
            self.model = genai.GenerativeModel('gemini-pro')
        except Exception as e:
            print(f"Error configuring Generative AI: {e}")
            self.model = None

        self.agent_persona = """
        Você é um agente especializado para atendimento dos clientes de uma administradora de condomínio.
        Sua função é identificar a intenção do usuário e retornar um dos seguintes comandos:
        - abrir_chamado
        - consultar_status
        - segunda_via_boleto
        - consultar_dados
        - reservar_area
        - duvidas_frequentes
        - negociar_inadimplencia
        - autoatendimento_comercial
        - fallback (se não entender a intenção)

        Responda apenas com o comando. Exemplo: se o usuário disser 'quero abrir um chamado', responda 'abrir_chamado'.
        """

    def get_intent(self, text):
        """
        This function will use a generative model to analyze the user's text and return the intent.
        """
        if not self.model:
            return {"intent": "fallback", "error": "Model not configured"}

        prompt = self.agent_persona + "\n\nUsuário: " + text + "\nIntenção:"

        try:
            response = self.model.generate_content(prompt)
            intent = response.text.strip()
            # Basic validation to ensure the model returns a valid intent
            valid_intents = [
                "abrir_chamado", "consultar_status", "segunda_via_boleto",
                "consultar_dados", "reservar_area", "duvidas_frequentes",
                "negociar_inadimplencia", "autoatendimento_comercial", "fallback"
            ]
            if intent not in valid_intents:
                return {"intent": "fallback", "original_response": intent}
            return {"intent": intent}
        except Exception as e:
            print(f"Error getting intent from model: {e}")
            return {"intent": "fallback", "error": str(e)}
