# dentro de core/chatbot.py

import random
from core.historico import Historico
from core.aprendizado import Aprendizado
from core.personalidade import Personalidade
from core.estatisticas import Estatisticas

class ChatBot:
    """Classe principal do ChatBot UFCA."""

    def __init__(self, base_conhecimento):
        self.base_conhecimento = base_conhecimento
        self.historico = Historico()
        self.aprendizado = Aprendizado()
        self.personalidade = Personalidade()
        self.perguntas_chaves_sessao = []

    # ## <-- MÉTODO CORRIGIDO
    def encontrar_resposta_predefinida(self, pergunta):
        """
        Encontra uma resposta buscando pela CORRESPONDÊNCIA EXATA da pergunta.
        Ideal para a interface de botões.
        """
        pergunta_lower = pergunta.lower()
        for item in self.base_conhecimento[self.personalidade.atual]:
            # ALTERAÇÃO PRINCIPAL: Compara a pergunta inteira, ignorando maiúsculas/minúsculas
            if item["pergunta"].lower() == pergunta_lower:
                self.perguntas_chaves_sessao.append(item["pergunta"])
                self.personalidade.registrar_uso_personalidade_atual()
                return random.choice(item["resposta"])
        
        # Fallback caso algo dê muito errado e a pergunta do botão não seja encontrada no JSON
        return "Desculpe, ocorreu um erro e não encontrei uma resposta para esta pergunta."

    def processar_pergunta_customizada(self, pergunta):
        pergunta_lower = pergunta.lower()
        # 1. Busca exata na base principal
        for personalidade_data in self.base_conhecimento.values():
            for item in personalidade_data:
                if item["pergunta"].lower() == pergunta_lower:
                    respostas_da_personalidade_atual = next(
                        (p["resposta"] for p in self.base_conhecimento[self.personalidade.atual] if p["pergunta"].lower() == pergunta_lower),
                        item["resposta"]
                    )
                    self.perguntas_chaves_sessao.append(item["pergunta"])
                    self.personalidade.registrar_uso_personalidade_atual()
                    return random.choice(respostas_da_personalidade_atual)

        # 2. Busca exata no aprendizado
        for item in self.aprendizado.dados:
            if item["pergunta"].lower() == pergunta_lower:
                self.perguntas_chaves_sessao.append(item["pergunta"])
                self.personalidade.registrar_uso_personalidade_atual()
                return item["resposta"]

        # 3. Fluxo de aprendizado
        self.perguntas_chaves_sessao.append("(Pergunta para Aprendizado)")
        return None

    def iniciar(self):
        # (Este método permanece como está para a versão terminal)
        pass # A lógica completa está nos arquivos que você já tem