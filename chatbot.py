import random

import json

import os
with open('json_chatbot.json', 'r', encoding='utf-8') as arq:
    dados = json.load(arq)

# Arquivo para novas duvidas
arquivo_novas_duvidas = 'novas_duvidas.json'

#Se já existir um arquivo, ele faz o load do existente para não perder nenhuma dúvida anterior
if os.path.exists(arquivo_novas_duvidas):
    with open(arquivo_novas_duvidas, 'r', encoding= 'utf-8') as arq:
        novas_duvidas = json.load(arq)
else:
    novas_duvidas = []


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
        if duvida not in novas_duvidas and duvida != "":
            novas_duvidas.append(duvida)
            with open(arquivo_novas_duvidas, 'w', encoding='utf-8') as arq:
                json.dump(novas_duvidas,arq,ensure_ascii=False,indent=4)
        return "Desculpa, ainda não sei responder a essa dúvida, mas guardei para analisar depois"



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