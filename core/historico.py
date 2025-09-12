import os

class Historico:
    """Gerencia o histórico de conversas."""

    def __init__(self, arquivo="data/historico_chat.txt"):
        self.arquivo = arquivo

    def salvar(self, pergunta, resposta):
        with open(self.arquivo, 'a', encoding='utf-8') as arq:
            arq.write(f"Usuário:  {pergunta}\n")
            arq.write(f"Chatbot: {resposta}\n")
            arq.write("=" * 50 + '\n')

    def ler_ultimas_interacoes(self, n=5):
        if not os.path.exists(self.arquivo):
            return []
        with open(self.arquivo, 'r', encoding='utf-8') as arq:
            linhas = arq.readlines()
        interacoes = [linhas[i:i+3] for i in range(0, len(linhas), 3)]
        return interacoes[-n:]

    def mostrar_ultimas_interacoes(self):
        ultimas = self.ler_ultimas_interacoes()
        if ultimas:
            print("Últimas interações.", "\n", "=" * 50)
            for interacao in ultimas:
                for linha in interacao:
                    print(linha, end="")
            print("=" * 50 + "\n")