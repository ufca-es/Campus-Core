import random
from core.historico import Historico
from core.aprendizado import Aprendizado
from core.personalidade import Personalidade, detectar_personalidade
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

        # Aprendizado se não souber
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
                estatisticas = Estatisticas(
                    perguntas_chaves_sessao=self.perguntas_chaves_sessao,
                    contador_sessao=self.personalidade.contador_sessao,
                    contador_acumulado=self.personalidade.contador
                )
                estatisticas.mostrar()
                break

            nova_personalidade, pergunta_limpa = detectar_personalidade(duvida, self.personalidade.atual)
            self.personalidade.alterar(nova_personalidade)

            resposta = self.encontrar_resposta(pergunta_limpa)
            print(f"({self.personalidade.atual}) Chatbot:", resposta)
            self.historico.salvar(duvida, resposta)
            self.personalidade.salvar_contador()