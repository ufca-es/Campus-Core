# estatisticas.py

import os
from collections import Counter

class Estatisticas:
    """Exibe estatísticas de uso do chatbot."""

    # Adicionado base_conhecimento e historico_path para análise completa
    def __init__(self, perguntas_chaves_sessao, contador_sessao, contador_acumulado, base_conhecimento, historico_path="data/historico_chat.txt"):
        self.perguntas_chaves_sessao = perguntas_chaves_sessao
        self.contador_sessao = contador_sessao
        self.contador_acumulado = contador_acumulado
        self.base_conhecimento = base_conhecimento # NOVO
        self.historico_path = historico_path # NOVO

    # Método para mapear uma pergunta do usuário à sua pergunta-chave no JSON
    def _mapear_pergunta_para_chave(self, pergunta_usuario):
        pergunta_lower = pergunta_usuario.lower()
        # Itera sobre todas as personalidades e perguntas na base de conhecimento
        for personalidade in self.base_conhecimento.values():
            for item in personalidade:
                if "keywords" in item:
                    for kw in item["keywords"]:
                        if kw in pergunta_lower:
                            return item["pergunta"] # Retorna a pergunta-chave
        return None

    # Método principal para gerar e exibir as sugestões
    def sugerir_perguntas_frequentes(self, top_n=3):
        print("\n=== Sugestões de Perguntas Frequentes ===")
        
        if not os.path.exists(self.historico_path):
            print("Ainda não há histórico de conversas para gerar sugestões. Use o chatbot e tente novamente!")
            print("======================================\n")
            return

        with open(self.historico_path, 'r', encoding='utf-8') as arq:
            linhas = arq.readlines()

        perguntas_usuarios = [linha.replace("Usuário: ", "").strip() for linha in linhas if linha.startswith("Usuário:")]

        if not perguntas_usuarios:
            print("Não foram encontradas perguntas no histórico.")
            print("======================================\n")
            return

        perguntas_chaves_mapeadas = []
        for p in perguntas_usuarios:
            chave = self._mapear_pergunta_para_chave(p)
            if chave:
                perguntas_chaves_mapeadas.append(chave)

        if not perguntas_chaves_mapeadas:
            print("Não foi possível mapear perguntas do histórico para a base de conhecimento.")
            print("======================================\n")
            return
            
        contador_historico = Counter(perguntas_chaves_mapeadas)
        mais_comuns = contador_historico.most_common(top_n)

        print("Com base no histórico, os usuários costumam perguntar sobre:")
        for i, (pergunta, _) in enumerate(mais_comuns):
            print(f"{i+1}. {pergunta}")
        print("======================================\n")


    def mostrar(self):
        print("\n=== Estatística da Sessão Atual ===")
        total = len(self.perguntas_chaves_sessao)
        print(f"Total de interações: {total}")

        if self.perguntas_chaves_sessao:
            contador = Counter(self.perguntas_chaves_sessao)
            pergunta_mais_frequente, vezes = contador.most_common(1)[0]
            print(f"Pergunta mais feita nesta sessão: '{pergunta_mais_frequente}' ({vezes} vezes)")

        print("\nUso das personalidades nesta sessão:")
        for persona, qtd in self.contador_sessao.items():
            print(f"- {persona}: {qtd} vez(es)")

        print("\nUso acumulado das personalidades:")
        for persona, qtd in self.contador_acumulado.items():
            print(f"- {persona}: {qtd} vez(es)")
        print("==================================\n")