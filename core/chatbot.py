import random
from core.historico import Historico
from core.aprendizado import Aprendizado
from core.personalidade import Personalidade
# Removido 'detectar_personalidade' e relatórios, pois não são usados diretamente na classe
from core.estatisticas import Estatisticas

class ChatBot:
    """Classe principal do ChatBot UFCA."""

    def __init__(self, base_conhecimento):
        self.base_conhecimento = base_conhecimento
        self.historico = Historico()
        self.aprendizado = Aprendizado()
        self.personalidade = Personalidade()
        self.perguntas_chaves_sessao = []

    def encontrar_resposta_predefinida(self, pergunta):
        pergunta_lower = pergunta.lower()
        for item in self.base_conhecimento[self.personalidade.atual]:
            if "keywords" in item:
                for kw in item["keywords"]:
                    if kw in pergunta_lower:
                        self.perguntas_chaves_sessao.append(item["pergunta"])
                        # ## <-- CORREÇÃO APLICADA AQUI
                        self.personalidade.registrar_uso_personalidade_atual()
                        return random.choice(item["resposta"])
        return "Desculpe, não encontrei uma resposta para esta pergunta pré-definida."

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
                    # ## <-- CORREÇÃO APLICADA AQUI
                    self.personalidade.registrar_uso_personalidade_atual()
                    return random.choice(respostas_da_personalidade_atual)

        # 2. Busca exata no aprendizado
        for item in self.aprendizado.dados:
            if item["pergunta"].lower() == pergunta_lower:
                self.perguntas_chaves_sessao.append(item["pergunta"])
                # ## <-- CORREÇÃO APLICADA AQUI
                self.personalidade.registrar_uso_personalidade_atual()
                return item["resposta"]

        # 3. Fluxo de aprendizado
        self.perguntas_chaves_sessao.append("(Pergunta para Aprendizado)")
        return None

    def iniciar(self):
        # (Este método permanece como está para a versão terminal)
        pass # A lógica completa está nos arquivos que você já tem