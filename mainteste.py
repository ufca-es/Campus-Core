import json
# Importa o módulo 'random' para permitir o sorteio de respostas.
import random

def extrair_perguntas_unicas(dados_chatbot):
    perguntas_set = set()
    for persona in dados_chatbot.values():
        for item in persona:
            perguntas_set.add(item['pergunta'])
    return list(perguntas_set)

def escolha_persona():
    while True:
        try:
            print("\nCom qual personalidade devo responder?")
            print("1. Engraçado\n2. Formal\n3. Rude")
            
            persona_num = int(input("Sua Escolha: "))
            
            if persona_num == 1:
                return "Engracado"
            elif persona_num == 2:
                return "Formal"
            elif persona_num == 3:
                return "Rude"
            else:
                print("Escolha de personalidade inválida. Tente novamente.")
        except ValueError:
            print("Entrada inválida. Por favor, digite um número.")

def encontrar_resposta(pergunta_escolhida, persona_escolhida, dados_chatbot):
    for item in dados_chatbot[persona_escolhida]:
        if item['pergunta'] == pergunta_escolhida:
            # Sorteia e retorna um item aleatório da lista de respostas.
            return random.choice(item['resposta'])
    return "Resposta não encontrada."

# --- Início do programa ---

print("Bem-Vindo ao chat Bot da UFCA\n")

# Carrega os dados do seu novo arquivo JSON.
with open('json_chatbot.json', 'r', encoding='utf-8') as arq:
    dados = json.load(arq)

# Gera a lista de todas as perguntas disponíveis, incluindo as novas.
perguntas_disponiveis = extrair_perguntas_unicas(dados)

# Loop principal da conversa.
while True:
    print("\nPerguntas Principais. (Digite o número da pergunta para escolher):")
    for i, pergunta in enumerate(perguntas_disponiveis, start=1):
        print(f"{i}. {pergunta}") 
    print("0. Sair")

    try:
        escolha_num = int(input("\nSua escolha: "))

        if 1 <= escolha_num <= len(perguntas_disponiveis):
            pergunta_selecionada = perguntas_disponiveis[escolha_num - 1]
            
            persona_selecionada = escolha_persona()
            
            # A função agora retorna uma resposta sorteada.
            resposta = encontrar_resposta(pergunta_selecionada, persona_selecionada, dados)
            print(f"\n>> Resposta ({persona_selecionada}): {resposta}")

        elif escolha_num == 0:
            print("\nSaindo...")
            break
        else:
            print("\nOpção inválida. Tente novamente.")
    except ValueError:
        print("\nEntrada inválida. Por favor, digite um número.")