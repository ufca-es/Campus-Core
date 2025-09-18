# dentro de core/estatisticas.py

import os
from collections import Counter

class Estatisticas:
    """Exibe e calcula estatísticas de uso do chatbot."""

    def __init__(self, perguntas_chaves_sessao, contador_sessao, contador_acumulado, base_conhecimento, historico_path="data/historico_chat.txt"):
        self.perguntas_chaves_sessao = perguntas_chaves_sessao
        self.contador_sessao = contador_sessao
        self.contador_acumulado = contador_acumulado
        self.base_conhecimento = base_conhecimento
        self.historico_path = historico_path

    def _mapear_pergunta_para_chave(self, pergunta_usuario):
        pergunta_lower = pergunta_usuario.lower()
        for personalidade in self.base_conhecimento.values():
            for item in personalidade:
                if "keywords" in item:
                    for kw in item["keywords"]:
                        if kw in pergunta_lower:
                            return item["pergunta"]
        return None

    # ## <-- MÉTODO MODIFICADO: Agora retorna uma lista em vez de imprimir
    def obter_sugestoes_perguntas(self, top_n=3):
        """
        Analisa o histórico completo e retorna uma lista com as top_n perguntas mais frequentes.
        """
        if not os.path.exists(self.historico_path):
            return [] # Retorna lista vazia se não há histórico

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

        # Retorna apenas a string da pergunta para cada item na lista dos mais comuns
        return [pergunta for pergunta, _ in mais_comuns]

    def mostrar(self):
        # (Este método para a versão terminal permanece inalterado)
        print("\n=== Estatística da Sessão Atual ===")
        # ... (código existente)