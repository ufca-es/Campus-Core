import json
import os

keywords_personalidade = {
    "Engracado": ["engracado", "divertido", "brincalhão", "engracada", "engraçada", "engraçado"],
    "Formal": ["formal", "sério", "profissional"],
    "Rude": ["rude", "grosso", "sarcástico"]
}

class Personalidade:
    """Controla a personalidade do chatbot e estatísticas de uso."""

    def __init__(self, arquivo="data/contador_personalidades.json"):
        self.arquivo = arquivo
        self.atual = "Formal"
        self.contador = self._carregar()
        self.contador_sessao = {"Formal": 0, "Engracado": 0, "Rude": 0}

    def _carregar(self):
        if os.path.exists(self.arquivo):
            with open(self.arquivo, "r", encoding="utf-8") as arq:
                return json.load(arq)
        return {"Formal": 0, "Engracado": 0, "Rude": 0}

    def alterar(self, nova_personalidade):
        """Troca a personalidade atual e atualiza contadores."""
        self.atual = nova_personalidade
        self.contador[self.atual] += 1
        self.contador_sessao[self.atual] += 1

    def salvar_contador(self):
        """Persiste o contador acumulado em arquivo JSON."""
        with open(self.arquivo, "w", encoding="utf-8") as arq:
            json.dump(self.contador, arq, ensure_ascii=False, indent=4)

def detectar_personalidade(entrada, personalidade_atual="Formal"):
    """
    Detecta se o usuário solicitou troca de personalidade.
    Retorna (personalidade_detectada, entrada_limpa)
    """
    entrada_lower = entrada.lower()
    for persona, keywords in keywords_personalidade.items():
        for kw in keywords:
            if kw in entrada_lower:
                entrada = entrada_lower.replace(kw, "").strip()
                return persona, entrada
    return personalidade_atual, entrada