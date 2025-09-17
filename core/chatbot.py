# chatbot.py

import random
from core.historico import Historico
from core.aprendizado import Aprendizado
from core.personalidade import Personalidade, detectar_personalidade
from core.relatorio import gerar_relatorio_final
from core.estatisticas import Estatisticas

class ChatBot:
    """Classe principal do ChatBot UFCA."""

    def __init__(self, base_conhecimento):
        self.base_conhecimento = base_conhecimento
        self.historico = Historico()
        self.aprendizado = Aprendizado()
        self.personalidade = Personalidade()
        self.perguntas_chaves_sessao = []

    def encontrar_resposta(self, pergunta):
        respostas_possiveis = []
        pergunta_chave = None
        pergunta_lower = pergunta.lower()

        for item in self.base_conhecimento[self.personalidade.atual]:
            if "keywords" in item:
                for kw in item["keywords"]:
                    if kw in pergunta_lower:
                        respostas_possiveis.extend(item["resposta"])
                        pergunta_chave = item["pergunta"]
                        break

        for item in self.aprendizado.dados:
            if item["pergunta"].lower() in pergunta_lower:
                respostas_possiveis.append(item["resposta"])
                pergunta_chave = item["pergunta"]

        if respostas_possiveis:
            if pergunta_chave:
                self.perguntas_chaves_sessao.append(pergunta_chave)
            return random.choice(respostas_possiveis)

        print("Não sei responder a essa dúvida. Poderia me dizer uma possível resposta?")
        sugestao = input("Diga sua sugestão: ")
        self.aprendizado.salvar_novo_conhecimento(pergunta, sugestao)
        return "Obrigado! Aprendi algo novo. Na próxima vez já vou saber responder."

    def iniciar(self):
        """Loop principal de interação com o usuário."""
        self.historico.mostrar_ultimas_interacoes()
        print("Bem-vindo ao ChatBot UFCA! Você pode digitar qualquer pergunta.\n")
        print("Para mudar a personalidade, use palavras como: engraçado, formal, rude.\nDigite 'sair' para encerrar.")

        while True:
            duvida = input("Digite sua dúvida: ")
            if duvida.lower() == "sair":
                print("Chatbot: Até logo")

                #Passa a base_conhecimento para a classe Estatisticas
                estatisticas = Estatisticas(
                    perguntas_chaves_sessao=self.perguntas_chaves_sessao,
                    contador_sessao=self.personalidade.contador_sessao,
                    contador_acumulado=self.personalidade.contador,
                    base_conhecimento=self.base_conhecimento,
                    historico_path=self.historico.arquivo  
                )
                
                # Chama o método para mostrar as sugestões antes das estatísticas
                estatisticas.sugerir_perguntas_frequentes()

                # A exibição das estatísticas da sessão e o relatório final continuam como antes
                estatisticas.mostrar() # Mostra estatísticas da sessão
                gerar_relatorio_final(estatisticas) # Gera o relatório
                break
            
            nova_personalidade, pergunta_limpa = detectar_personalidade(duvida, self.personalidade.atual)
            personalidade_mudou = nova_personalidade != self.personalidade.atual

            # --- Lógica de Personalidade e Feedback ---
            # Caixa Externa: Verificamos se a personalidade mudou PRIMEIRO.
            if personalidade_mudou:
                self.personalidade.alterar(nova_personalidade)
                self.personalidade.salvar_contador()
                
                # Caixa Interna: AGORA decidimos o feedback, pois SABEMOS que a personalidade mudou.
                # CASO 1: Mudou E HÁ uma pergunta junto.
                if pergunta_limpa.strip():
                    print(f"Chatbot: Personalidade alterada para {self.personalidade.atual}.")
                    # Corrigido: com 2 argumentos
                    self.historico.salvar(f"({duvida} -> Mudou para {self.personalidade.atual})", "(Ação de sistema)")
                
                # CASO 2: Mudou e era SÓ um comando.
                else:
                    print(f"({self.personalidade.atual}) Chatbot: Personalidade alterada. Como posso ajudar?")
                    self.historico.salvar(duvida, "(Comando para alterar personalidade)")
                    continue

            # Se a pergunta está vazia e a personalidade NÃO mudou (comando repetido),
            # simplesmente pulamos para a próxima.
            if not pergunta_limpa.strip():
                continue

            # --- Lógica para Responder Perguntas ---
            # Se chegamos aqui, é porque há uma pergunta real para ser respondida.
            resposta = self.encontrar_resposta(pergunta_limpa)
            print(f"({self.personalidade.atual}) Chatbot: {resposta}")
            self.historico.salvar(duvida, resposta)

