# dentro de core/personalidade.py

import json
import os

keywords_personalidade = {
    "Engracado": ["engracado", "divertido", "brincalhão", "engracada", "engraçada", "engraçado","brincalhao"],
    "Formal": ["formalidade","formal", "sério", "profissional"],
    "Rude": ["rude", "grosso", "sarcástico","sarcastico"]
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

    # ## <-- MÉTODO SIMPLIFICADO: Agora só define a personalidade
    def definir_personalidade_atual(self, nova_personalidade):
        """Apenas troca a personalidade atual, sem contar."""
        self.atual = nova_personalidade

    # ## <-- NOVO MÉTODO: Responsável por registrar o uso
    def registrar_uso_personalidade_atual(self):
        """Incrementa os contadores da personalidade atualmente em uso."""
        if self.atual in self.contador:
            self.contador[self.atual] += 1
            self.contador_sessao[self.atual] += 1
            self.salvar_contador() # Salva o contador acumulado

    def salvar_contador(self):
        """Persiste o contador acumulado em arquivo JSON."""
        with open(self.arquivo, "w", encoding="utf-8") as arq:
            json.dump(self.contador, arq, ensure_ascii=False, indent=4)

def detectar_personalidade(entrada, personalidade_atual="Formal"):
    # (Esta função auxiliar não precisa de alterações)
    entrada_lower = entrada.lower()
    for persona, keywords in keywords_personalidade.items():
        for kw in keywords:
            if kw in entrada_lower:
                entrada = entrada_lower.replace(kw, "").strip()
                return persona, entrada
    return personalidade_atual, entrada