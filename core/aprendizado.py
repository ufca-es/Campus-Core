import json
import os

class Aprendizado:
    """Gerencia aprendizado incremental do chatbot."""

    def __init__(self, arquivo="data/aprendizado.json"):
        self.arquivo = arquivo
        self.dados = self._carregar()

    def _carregar(self):
        if os.path.exists(self.arquivo):
            with open(self.arquivo, 'r', encoding='utf-8') as arq:
                return json.load(arq)
        return []

    def salvar_novo_conhecimento(self, pergunta, resposta):
        novo_conhecimento = {"pergunta": pergunta, "resposta": resposta}
        self.dados.append(novo_conhecimento)
        with open(self.arquivo, 'w', encoding='utf-8') as arq:
            json.dump(self.dados, arq, ensure_ascii=False, indent=4)