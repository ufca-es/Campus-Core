# core/personalidade.py (VERSÃO CORRIGIDA E UNIFICADA)
import json
import os

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

    def definir_personalidade(self, nova_personalidade, verbose=False):
        """
        Método unificado e corrigido para trocar de personalidade.
        - Valida se a personalidade existe.
        - Evita trocar para a mesma personalidade.
        - Se 'verbose' for True, imprime mensagens (para o terminal).
        """
        # 1. Valida se a personalidade solicitada é válida
        if nova_personalidade not in self.contador:
            if verbose:
                print(f"\nERRO: Personalidade '{nova_personalidade}' é inválida.")
            return

        # 2. Verifica se já não é a personalidade atual
        if self.atual == nova_personalidade:
            if verbose:
                print(f"\nA personalidade já é {self.atual}.")
            return

        # 3. Se for válida e diferente, realiza a troca
        self.atual = nova_personalidade
        if verbose:
            print(f"\nPersonalidade alterada para {self.atual}.")

    def registrar_uso_personalidade_atual(self):
        """Incrementa os contadores da personalidade em uso."""
        self.contador[self.atual] = self.contador.get(self.atual, 0) + 1
        self.contador_sessao[self.atual] = self.contador_sessao.get(self.atual, 0) + 1

    def salvar_contador(self):
        """Persiste o contador acumulado em arquivo JSON."""
        with open(self.arquivo, "w", encoding="utf-8") as arq:
            json.dump(self.contador, arq, ensure_ascii=False, indent=4)