"""Módulo responsável por gerar estatísticas de uso do chatbot."""

import os
from collections import Counter

class Estatisticas:
    """Calcula e exibe estatísticas de uso com base no histórico de conversas."""

    def __init__(self, perguntas_chaves_sessao, contador_sessao, contador_acumulado, base_conhecimento, historico_path="data/historico_chat.txt"):
        """
        Inicializa a classe de estatísticas.

        Args:
            perguntas_chaves_sessao (list): Lista de perguntas feitas na sessão atual.
            contador_sessao (dict): Contagem de uso das personalidades na sessão.
            contador_acumulado (dict): Contagem de uso das personalidades acumulado.
            base_conhecimento (dict): Base de conhecimento do chatbot.
            historico_path (str): Caminho para o arquivo de histórico.
        """
        self.perguntas_chaves_sessao = perguntas_chaves_sessao
        self.contador_sessao = contador_sessao
        self.contador_acumulado = contador_acumulado
        self.base_conhecimento = base_conhecimento
        self.historico_path = historico_path

    def _mapear_pergunta_para_chave(self, pergunta_usuario):
        """
        Mapeia uma pergunta do usuário para uma chave de pergunta conhecida.

        Args:
            pergunta_usuario (str): Texto da pergunta do usuário.

        Returns:
            str | None: Pergunta mapeada ou None se não encontrada.
        """
        pergunta_lower = pergunta_usuario.lower()
        for personalidade in self.base_conhecimento.values():
            for item in personalidade:
                if "keywords" in item:
                    for kw in item["keywords"]:
                        if kw in pergunta_lower:
                            return item["pergunta"]
        return None

    def obter_sugestoes_perguntas(self, top_n=3):
        """
        Retorna uma lista com as perguntas mais frequentes do histórico.

        Args:
            top_n (int): Número de perguntas mais comuns a retornar.

        Returns:
            list: Lista de perguntas mais frequentes.
        """
        if not os.path.exists(self.historico_path):
            return []
        with open(self.historico_path, 'r', encoding='utf-8') as arq:
            linhas = arq.readlines()

        perguntas_usuarios = [linha.replace("Usuário: ", "").strip() for linha in linhas if linha.startswith("Usuário:")]
        if not perguntas_usuarios:
            return []

        perguntas_chaves_mapeadas = []
        for p in perguntas_usuarios:
            chave = self._mapear_pergunta_para_chave(p)
            if chave:
                perguntas_chaves_mapeadas.append(chave)
        
        if not perguntas_chaves_mapeadas:
            return []
            
        contador_historico = Counter(perguntas_chaves_mapeadas)
        mais_comuns = contador_historico.most_common(top_n)
        return [pergunta for pergunta, _ in mais_comuns]

    def mostrar(self):
        """Mostra estatísticas da sessão atual (versão terminal)."""
        print("\n=== Estatística da Sessão Atual ===")
        # ... código existente
