"""Módulo responsável por gerenciar o histórico de conversas do chatbot."""

import os

class Historico:
    """Gerencia o armazenamento e leitura do histórico de interações entre usuário e chatbot."""

    def __init__(self, arquivo="data/historico_chat.txt"):
        """
        Inicializa a classe Historico.

        Args:
            arquivo (str): Caminho do arquivo de histórico.
        """
        self.arquivo = arquivo

    def salvar(self, pergunta, resposta):
        """
        Salva uma interação no arquivo de histórico.

        Args:
            pergunta (str): Pergunta feita pelo usuário.
            resposta (str): Resposta fornecida pelo chatbot.
        """
        with open(self.arquivo, 'a', encoding='utf-8') as arq:
            arq.write(f"Usuário:  {pergunta}\n")
            arq.write(f"Chatbot: {resposta}\n")
            arq.write("=" * 50 + '\n')

    def ler_ultimas_interacoes(self, n=5):
        """
        Lê as últimas interações registradas no histórico.

        Args:
            n (int): Número de interações a serem retornadas.

        Returns:
            list: Lista contendo blocos de interações (pergunta, resposta e separador).
        """
        if not os.path.exists(self.arquivo):
            return []
        with open(self.arquivo, 'r', encoding='utf-8') as arq:
            linhas = arq.readlines()
        interacoes = [linhas[i:i+3] for i in range(0, len(linhas), 3)]
        return interacoes[-n:]

    def mostrar_ultimas_interacoes(self):
        """Exibe no terminal as últimas interações armazenadas no histórico."""
        ultimas = self.ler_ultimas_interacoes()
        if ultimas:
            print("Últimas interações.", "\n", "=" * 50)
            for interacao in ultimas:
                for linha in interacao:
                    print(linha, end="")
            print("=" * 50 + "\n")
