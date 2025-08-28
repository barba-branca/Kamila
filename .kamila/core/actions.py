class Actions:
    def __init__(self, tts_engine):
        self.tts_engine = tts_engine

    def execute(self, intent_data, context):
        intent = intent_data.get("intent")

        action_map = {
            "abrir_chamado": self.abrir_chamado,
            "consultar_status": self.consultar_status,
            "segunda_via_boleto": self.segunda_via_boleto,
            "consultar_dados": self.consultar_dados,
            "reservar_area": self.reservar_area,
            "duvidas_frequentes": self.duvidas_frequentes,
            "negociar_inadimplencia": self.negociar_inadimplencia,
            "autoatendimento_comercial": self.autoatendimento_comercial,
        }

        action = action_map.get(intent, self.fallback)
        return action(context)

    def _speak_and_return(self, response, next_state, context):
        print(response)
        self.tts_engine.speak(response)
        return next_state, context

    def abrir_chamado(self, context):
        return self._speak_and_return(
            "Entendido. Para qual departamento você gostaria de abrir o chamado?",
            "AWAITING_DEPARTMENT",
            context
        )

    def consultar_status(self, context):
        return self._speak_and_return(
            "Para consultar o status, por favor, me informe o número do protocolo.",
            "AWAITING_PROTOCOL",
            context
        )

    def segunda_via_boleto(self, context):
        context['pending_action'] = 'send_boleto'
        return self._speak_and_return(
            "A segunda via do boleto será enviada para o seu email cadastrado. Confirma? (sim ou não)",
            "AWAITING_CONFIRMATION",
            context
        )

    def consultar_dados(self, context):
        return self._speak_and_return(
            "Para consultar seus dados, por favor, confirme seu nome completo.",
            "AWAITING_FULL_NAME",
            context
        )

    def reservar_area(self, context):
        return self._speak_and_return(
            "Qual área comum você gostaria de reservar?",
            "AWAITING_AREA_NAME",
            context
        )

    def duvidas_frequentes(self, context):
        return self._speak_and_return(
            "Qual é a sua dúvida? Fale livremente e tentarei ajudar.",
            "AWAITING_QUESTION",
            context
        )

    def negociar_inadimplencia(self, context):
        return self._speak_and_return(
            "Entendo. O setor de negociação entrará em contato. Posso confirmar o seu número de telefone?",
            "AWAITING_PHONE_CONFIRMATION",
            context
        )

    def autoatendimento_comercial(self, context):
        context['pending_action'] = 'commercial_lead'
        return self._speak_and_return(
            "Bem-vindo ao nosso autoatendimento. Você tem interesse em conhecer nossos serviços? (sim ou não)",
            "AWAITING_CONFIRMATION",
            context
        )

    def fallback(self, context):
        return self._speak_and_return(
            "Desculpe, não entendi. Como posso te ajudar?",
            "IDLE",
            context
        )
