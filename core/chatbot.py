# core/chatbot.py (VERSÃO UNIFICADA)

import random
from .historico import Historico
from .aprendizado import Aprendizado
from .personalidade import Personalidade
from .relatorio import gerar_relatorio_final
from .estatisticas import Estatisticas

class ChatBot:
    """Classe principal do ChatBot UFCA, compatível com Terminal e Streamlit."""

    def __init__(self, base_conhecimento):
        self.base_conhecimento = base_conhecimento
        self.historico = Historico()
        self.aprendizado = Aprendizado()
        self.personalidade = Personalidade()
        self.perguntas_chaves_sessao = []

    def encontrar_resposta(self, pergunta, interactive_mode=False):
        """
        Método unificado para encontrar respostas.
        - Usa busca por keywords.
        - Se 'interactive_mode' for True, usa print/input para aprender.
        - Se for False, retorna None para a interface gráfica gerenciar o aprendizado.
        """
        respostas_possiveis = []
        pergunta_chave = None
        pergunta_lower = pergunta.lower()

        # Busca na base de conhecimento principal por keywords
        for item in self.base_conhecimento.get(self.personalidade.atual, []):
            if any(kw in pergunta_lower for kw in item.get("keywords", [])):
                respostas_possiveis.extend(item["resposta"])
                pergunta_chave = item["pergunta"]
                break  # Para na primeira correspondência para ser mais direto

        # Se não achou, busca no conhecimento aprendido
        if not respostas_possiveis:
            for item in self.aprendizado.dados:
                if item["pergunta"].lower() in pergunta_lower:
                    respostas_possiveis.append(item["resposta"])
                    pergunta_chave = item["pergunta"]

        if respostas_possiveis:
            if pergunta_chave:
                self.perguntas_chaves_sessao.append(pergunta_chave)
            self.personalidade.registrar_uso_personalidade_atual()
            return random.choice(respostas_possiveis)

        # Se não encontrou resposta em lugar nenhum
        self.perguntas_chaves_sessao.append("(Pergunta para Aprendizado)")

        if interactive_mode:
            # FLUXO DE APRENDIZADO PARA O TERMINAL
            print("\nEssa informação não consta no meu banco de dados.")
            print("Deseja me ensinar uma possível resposta?\n1. Sim\n2. Não")
            escolha_aprender = input("Opção: ")
            if escolha_aprender == '1':
                sugestao = input("\nQual seria uma boa resposta para essa pergunta? ")
                self.aprendizado.salvar_novo_conhecimento(pergunta, sugestao)
                self.historico.salvar(f"(Aprendendo): {pergunta}", f"(Sugestão): {sugestao}")
                return "Obrigado! Aprendi algo novo com a sua ajuda."
            else:
                return "Entendido! Sem problemas."
        else:
            # RETORNO PARA A INTERFACE GRÁFICA
            return None

    def menu_mudar_personalidade(self):
        """Menu para o modo terminal."""
        print("\n--- Escolha a nova personalidade ---\n1. Formal\n2. Engracado\n3. Rude\nQualquer outra tecla para cancelar.")
        escolha = input("Opção: ")
        if escolha == "1":
            self.personalidade.definir_personalidade("Formal", verbose=True)
        elif escolha == "2":
            self.personalidade.definir_personalidade("Engracado", verbose=True)
        elif escolha == "3":
            self.personalidade.definir_personalidade("Rude", verbose=True)
        else:
            print("Seleção cancelada.")

    def iniciar(self):
        """Loop principal de interação com o usuário no modo terminal."""
        self.historico.mostrar_ultimas_interacoes()
        print("Bem-vindo ao ChatBot UFCA! Você pode digitar qualquer pergunta.\n")

        while True:
            print(f"\n--- Menu Principal (Personalidade atual: {self.personalidade.atual}) ---")
            print("1. Fazer uma pergunta\n2. Mudar a personalidade\n3. Sair")
            escolha_menu = input("O que você deseja fazer? ")

            if escolha_menu == '1':
                duvida = input("\nDigite sua dúvida: ")
                resposta = self.encontrar_resposta(duvida, interactive_mode=True)
                print(f"\n({self.personalidade.atual}) Chatbot: {resposta}")
                if "Aprendendo" not in duvida: # Evita salvar o aprendizado duas vezes
                    self.historico.salvar(duvida, resposta)
            elif escolha_menu == '2':
                self.menu_mudar_personalidade()
            elif escolha_menu == '3':
                print("Chatbot: Até logo!")
                estatisticas = Estatisticas(
                    perguntas_chaves_sessao=self.perguntas_chaves_sessao,
                    contador_sessao=self.personalidade.contador_sessao,
                    contador_acumulado=self.personalidade.contador,
                    base_conhecimento=self.base_conhecimento,
                    historico_path=self.historico.arquivo
                )
                estatisticas.sugerir_perguntas_frequentes()
                estatisticas.mostrar()
                gerar_relatorio_final(estatisticas)
                break
            else:
                print("Opção inválida, por favor, escolha uma das opções do menu.")