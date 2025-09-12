from collections import Counter

class Estatisticas:
    """Exibe estatísticas de uso do chatbot."""

    def __init__(self, perguntas_chaves_sessao, contador_sessao, contador_acumulado):
        self.perguntas_chaves_sessao = perguntas_chaves_sessao
        self.contador_sessao = contador_sessao
        self.contador_acumulado = contador_acumulado

    def mostrar(self):
        print("\n=== Estatística da Sessão ===")
        total = len(self.perguntas_chaves_sessao)
        print(f"Total de interações: {total}")

        if self.perguntas_chaves_sessao:
            contador = Counter(self.perguntas_chaves_sessao)
            pergunta_mais_frequente, vezes = contador.most_common(1)[0]
            print(f"Pergunta mais feita: '{pergunta_mais_frequente}' ({vezes} vezes)")

        print("\nUso das personalidades nesta sessão:")
        for persona, qtd in self.contador_sessao.items():
            print(f"- {persona}: {qtd} vez(es)")

        print("\nUso acumulado das personalidades:")
        for persona, qtd in self.contador_acumulado.items():
            print(f"- {persona}: {qtd} vez(es)")
        print("==============================\n")