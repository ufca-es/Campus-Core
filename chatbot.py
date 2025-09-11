import random

import json

with open('json_chatbot.json', 'r', encoding='utf-8') as arq:
    dados = json.load(arq)


#Keywords para personalidades
keywords_personalidade = {
    "Engracado":["engracado", "divertido", "brincalhão", "engracada"],
    "Formal": ["formal", "sério", "profissional"],
    "Rude": ["rude", "grosso", "sarcástico"]
}


#Nova Escolha de personalidade

def detectar_personalidade(entrada, personalidade_atual="Formal"):
    entrada_lower = entrada.lower()
    for persona, keywords in keywords_personalidade.items():
        for kw in keywords:
            if kw in entrada_lower:
                entrada = entrada_lower.replace(kw,"").strip()
                return persona,entrada
    return personalidade_atual, entrada

#Escolher personalidade

# encontrar respostas.
def encontrar_respostas(duvida,personalidade):
    respostas_possiveis = []
    duvida_lower = duvida.lower()

    for item in dados[personalidade]:
        if "keywords" in item:
            for kw in item['keywords']:
                if kw in duvida_lower:
                    respostas_possiveis.extend(item['resposta'])
                    break
    if respostas_possiveis:
        return random.choice(respostas_possiveis)
    else:
        return "Desculpa, ainda não sei responder a essa dúvida, ou não consegui compreendela"



#Modificar essa função de escolher pergunta
        
def codigo_principal():
    personalidade_atual = "Formal"
    print("Bem-vindo ao ChatBot UFCA! Você pode digitar qualquer pergunta.\n")
    print("Para mudar a personalidade, use palavras como: engraçado, formal, rude.\nDigite sair para encerrar o programa")

    while True:
        duvida = input("Digite sua dúvida: ")
        if duvida.lower() == "sair":
            print("Chatbot: Até logo")
            break
        #Detectar a mudança de personalidade 
        personalidade_atual, duvida_limpa = detectar_personalidade(duvida, personalidade_atual)

        resposta = encontrar_respostas(duvida_limpa, personalidade_atual)

        print(f"({personalidade_atual}) Chatbot:", resposta)

#Chamar função principal

codigo_principal()