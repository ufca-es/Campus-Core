"""Módulo responsável por controlar a personalidade do chatbot e suas estatísticas de uso."""

import json
import os

keywords_personalidade = {
    "Engracado": ["engracado", "divertido", "brincalhão", "engracada", "engraçada", "engraçado", "brincalhao"],
    "Formal": ["formalidade", "formal", "sério", "profissional"],
    "Rude": ["rude", "grosso", "sarcástico", "sarcastico"]
}

class Personalidade:
    """Controla a personalidade ativa do chatbot e contabiliza seu uso."""

    def __init__(self, arquivo="data/contador_personalidades.json"):
        """
        Inicializa a classe Personalidade.

        Args:
            arquivo (str): Caminho para o arquivo JSON que armazena os contadores.
        """
        self.arquivo = arquivo
        self.atual = "Formal"
        self.contador = self._carregar()
        self.contador_sessao = {"Formal": 0, "Engracado": 0, "Rude": 0}

    def _carregar(self):
        """
        Carrega os contadores de uso das personalidades do arquivo.

        Returns:
            dict: Contador acumulado por personalidade.
        """
        if os.path.exists(self.arquivo):
            with open(self.arquivo, "r", encoding="utf-8") as arq:
                return json.load(arq)
        return {"Formal": 0, "Engracado": 0, "Rude": 0}

    def definir_personalidade_atual(self, nova_personalidade):
        """
        Define a personalidade ativa do chatbot.

        Args:
            nova_personalidade (str): Nome da personalidade a ser ativada.
        """
        self.atual = nova_personalidade

    def registrar_uso_personalidade_atual(self):
        """Incrementa o contador de uso para a personalidade atualmente ativa."""
        if self.atual in self.contador:
            self.contador[self.atual] += 1
            self.contador_sessao[self.atual] += 1
            self.salvar_contador()

    def salvar_contador(self):
        """Persiste o contador acumulado de uso em arquivo JSON."""
        with open(self.arquivo, "w", encoding="utf-8") as arq:
            json.dump(self.contador, arq, ensure_ascii=False, indent=4)

def detectar_personalidade(entrada, personalidade_atual="Formal"):
    """
    Detecta a personalidade com base em palavras-chave na entrada do usuário.

    Args:
        entrada (str): Texto digitado pelo usuário.
        personalidade_atual (str): Personalidade ativa no momento.

    Returns:
        tuple: (personalidade_detectada, entrada_sem_keywords)
    """
    entrada_lower = entrada.lower()
    for persona, keywords in keywords_personalidade.items():
        for kw in keywords:
            if kw in entrada_lower:
                entrada = entrada_lower.replace(kw, "").strip()
                return persona, entrada
    return personalidade_atual, entrada