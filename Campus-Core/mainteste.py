
def escolha_persona():
    while True:
        print("Digite:\n1. Engraçado\n2. Formal\n3.Rude\n")
        persona = int(input("Sua Escolha: "))
        match persona:
            case 1:
                print("Personalidade: Engraçada Escolhida.")
                return "Engracado"
                
            case 2:
                print("Personalidade: Formal Escolhida")
                return "Formal"
            case 3:
                print("Personalidade: Rude Escolhida.")
                return "Rude"
                
            case _:
                print("Escolha de personalidade inválida. Tente novamente:")

def escolha_pergunta(persona_escolhida):
    while True:
        print("\nPerguntas Principais. (Digite o número da pergunta para escolher): ")
        for i, item in enumerate(dados[persona_escolhida], start=1):
            print(f"{i}. {item['pergunta']}") 
        print("0. Sair")

        escolha_pergunta = int(input("Sua escolha: "))

        if escolha_pergunta >= 1 and escolha_pergunta <= len(dados[persona_escolhida]):
            resposta = dados[persona_escolhida][escolha_pergunta - 1]["resposta"]
            print(f"Resposta: {resposta}")

        elif escolha_pergunta == 0:
            print("saindo")
            break
        else:
            print("Opção inválida")

        
import json
print("Bem-Vindo ao chat Bot da UFCA\nSelecione uma das personalidades para começar.\n")
with open('json_chatbot.json', 'r', encoding='utf-8') as arq:
    dados = json.load(arq)

escolha_persona = escolha_persona()
escolha_pergunta(escolha_persona)