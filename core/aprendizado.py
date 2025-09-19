"""Módulo responsável pelo aprendizado incremental do chatbot."""

import json
import os

class Aprendizado:

    def __init__(self, arquivo="data/aprendizado.json"):
        """
        Inicializa a classe Aprendizado.

        Args:
            arquivo (str): Caminho do arquivo JSON que armazena os novos conhecimentos.
        """
        self.arquivo = arquivo
        self.dados = self._carregar()

    def _carregar(self):
        """
        Carrega os conhecimentos aprendidos a partir do arquivo JSON.

        Returns:
            list: Lista de dicionários contendo perguntas e respostas aprendidas.
        """
        if os.path.exists(self.arquivo):
            with open(self.arquivo, 'r', encoding='utf-8') as arq:
                return json.load(arq)
        return []

    def salvar_novo_conhecimento(self, pergunta, resposta):
        """
        Salva uma nova pergunta e resposta no arquivo de aprendizado.

        Args:
            pergunta (str): Pergunta fornecida pelo usuário.
            resposta (str): Resposta correspondente para ser aprendida.
        """
        novo_conhecimento = {"pergunta": pergunta, "resposta": resposta}
        self.dados.append(novo_conhecimento)
        with open(self.arquivo, 'w', encoding='utf-8') as arq:
            json.dump(self.dados, arq, ensure_ascii=False, indent=4)
