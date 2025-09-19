"""Módulo principal que define a classe ChatBot e gerencia interações com o usuário."""

import random
from core.historico import Historico
from core.aprendizado import Aprendizado
from core.personalidade import Personalidade
from core.estatisticas import Estatisticas

class ChatBot:
    """Classe principal do ChatBot UFCA, responsável por processar perguntas e gerenciar estado."""

    def __init__(self, base_conhecimento):
        """
        Inicializa o ChatBot.

        Args:
            base_conhecimento (dict): Base de conhecimento contendo perguntas e respostas.
        """
        self.base_conhecimento = base_conhecimento
        self.historico = Historico()
        self.aprendizado = Aprendizado()
        self.personalidade = Personalidade()
        self.perguntas_chaves_sessao = []

    def encontrar_resposta_predefinida(self, pergunta):
        """
        Encontra uma resposta buscando pela correspondência exata da pergunta.

        Ideal para a interface de botões.

        Args:
            pergunta (str): Pergunta do usuário.

        Returns:
            str: Resposta correspondente ou mensagem de erro.
        """
        pergunta_lower = pergunta.lower()
        for item in self.base_conhecimento[self.personalidade.atual]:
            if item["pergunta"].lower() == pergunta_lower:
                self.perguntas_chaves_sessao.append(item["pergunta"])
                self.personalidade.registrar_uso_personalidade_atual()
                return random.choice(item["resposta"])
        return "Desculpe, ocorreu um erro e não encontrei uma resposta para esta pergunta."

    def processar_pergunta_customizada(self, pergunta):
        """
        Processa perguntas digitadas pelo usuário, verificando em:
        1. Base principal.
        2. Conhecimento aprendido.
        3. Fluxo de aprendizado (caso não encontre).

        Args:
            pergunta (str): Pergunta digitada pelo usuário.

        Returns:
            str | None: Resposta encontrada ou None se precisa aprender.
        """
        pergunta_lower = pergunta.lower()
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

        for item in self.aprendizado.dados:
            if item["pergunta"].lower() == pergunta_lower:
                self.perguntas_chaves_sessao.append(item["pergunta"])
                self.personalidade.registrar_uso_personalidade_atual()
                return item["resposta"]

        self.perguntas_chaves_sessao.append("(Pergunta para Aprendizado)")
        return None

    def iniciar(self):
        """Método placeholder para execução em terminal (não implementado na versão web)."""
        pass
