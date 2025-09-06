
def escolha_persona():
    while True:
        print("Digite:\n1. Engraçado\n2. Formal\n3. Rude\n")
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
        print("9. Trocar personalidade")  

        escolha = int(input("Sua escolha: "))

        if 1 <= escolha <= len(dados[persona_escolhida]):
            resposta = dados[persona_escolhida][escolha - 1]["resposta"]
            print(f"Resposta: {resposta}")

        elif escolha == 0:
            print("Saindo...")
            break

        elif escolha == 9:  
            print("\nMudando de personalidade...")
            persona_escolhida = escolha_persona()  

        else:
            print("Opção inválida.")

        
import json
print("Bem-Vindo ao chat Bot da UFCA\nSelecione uma das personalidades para começar.\n")
with open('json_chatbot.json', 'r', encoding='utf-8') as arq:
    dados = json.load(arq)

escolha_persona_inicial = escolha_persona()
escolha_pergunta(escolha_persona_inicial)
