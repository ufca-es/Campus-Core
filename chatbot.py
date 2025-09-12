import random
import json
import os
from collections import Counter

with open('json_chatbot.json', 'r', encoding='utf-8') as arq:
    dados = json.load(arq)

# Arquivos
arquivo_historico = 'historico_chat.txt' #Arquivo para histórico - task 12 (Tendo que ser feita primeira)
arquivo_novas_duvidas = 'novas_duvidas.json' # Arquivo para novas duvidas
arquivo_aprendizado = "aprendizado.json" #arquivo para aprendizado.
arquivo_qtd_personalidades = "contador_personalidades.json"


# Contador acumulado das personalidades.
if os.path.exists(arquivo_qtd_personalidades):
    with open(arquivo_qtd_personalidades, 'r', encoding='utf-8') as arq:
        contador_personalidades = json.load(arq)
else:
    contador_personalidades = {"Formal":0,"Engracado":0,"Rude":0}



#Contador apenas da sessão atual
contador_personalidades_sessao = {"Formal":0,"Engracado":0,"Rude":0}
perguntas_chaves_sessao = []

#Novas dúvidas
#Se já existir um arquivo, ele faz o load do existente para não perder nenhuma dúvida anterior
if os.path.exists(arquivo_novas_duvidas):
    with open(arquivo_novas_duvidas, 'r', encoding= 'utf-8') as arq:
        novas_duvidas = json.load(arq)
else:
    novas_duvidas = []


#If do Aprendizado.
if os.path.exists(arquivo_aprendizado):
    with open(arquivo_aprendizado, 'r', encoding='utf-8') as arq:
        aprendizado = json.load(arq)
else:
    aprendizado = []

#Keywords para personalidades
keywords_personalidade = {
    "Engracado":["engracado", "divertido", "brincalhão", "engracada", "engraçada","engraçado"],
    "Formal": ["formal", "sério", "profissional"],
    "Rude": ["rude", "grosso", "sarcástico"]
}

#-------- Funções auxiliares -------#

def salvar_historico(pergunta,resposta):
    with open(arquivo_historico, 'a', encoding='utf-8') as arq:
        arq.write(f"Usuário:  {pergunta}\n")
        arq.write(f"Chatbot: {resposta}\n")
        arq.write("="*50 + '\n')

#detecta as personalidades de acordo com: keywords_personalidade
def detectar_personalidade(entrada, personalidade_atual="Formal"):
    entrada_lower = entrada.lower()
    for persona, keywords in keywords_personalidade.items():
        for kw in keywords:
            if kw in entrada_lower:
                entrada = entrada_lower.replace(kw,"").strip()
                return persona,entrada
    return personalidade_atual, entrada

#Ler as 5 últimas interações
def ler_ultimas_interacoes():
    if not os.path.exists(arquivo_historico):
        return []
    with open(arquivo_historico, 'r', encoding='utf-8') as arq:
        linhas = arq.readlines()
    # cada resposta guardada, são usadas 3 linhas no .txt
    interacoes = [linhas[i:i+3] for i in range(0, len(linhas), 3)]
    return interacoes[-5:] 

# encontrar respostas.
def encontrar_respostas(duvida,personalidade):
    respostas_possiveis = []
    duvida_lower = duvida.lower()
    pergunta_chave = None

    for item in dados[personalidade]:
        if "keywords" in item:
            for kw in item['keywords']:
                if kw in duvida_lower:
                    respostas_possiveis.extend(item['resposta'])
                    pergunta_chave = item['pergunta']
                    break

    for item in aprendizado:
        if item['pergunta'].lower() in duvida_lower:
            respostas_possiveis.append(item["resposta"])
            pergunta_chave = item['pergunta']

    if respostas_possiveis:
        if pergunta_chave:
            perguntas_chaves_sessao.append(pergunta_chave)

        return random.choice(respostas_possiveis)
    
    else:
        # Task 10: Reimplementada
        print("Não sei responder a essa dúvida. Poderia me dizer uma possível resposta ? ")
        sugestao_do_usuario = input("Diga sua sugestão: ")

        novo_conhecimento = {"pergunta": duvida, "resposta": sugestao_do_usuario}
        aprendizado.append(novo_conhecimento)

        with open(arquivo_aprendizado, 'w', encoding='utf-8') as arq:
            json.dump(aprendizado, arq, ensure_ascii=False, indent=4)

        return "Obrigado! Aprendi algo novo. Na próxima vez já vou saber responder."
    
#Mostrar estatísticas.
def mostrar_estatisticas():
    print("\n=== Estatísitca da Sessão ===")
    total_interacoes = len(perguntas_chaves_sessao)
    print(f"Total de interações: {total_interacoes}")

    if perguntas_chaves_sessao:
        contador = Counter(perguntas_chaves_sessao)
        pergunta_mais_frequente,vezes = contador.most_common(1)[0]
        print(f"Pergunta mais feita: '{pergunta_mais_frequente}' ({vezes} vezes)")

    print("\nUso das personalidades nesta sessão:")
    for persona, qtd in contador_personalidades_sessao.items():
        print(f"- {persona}: {qtd} vez(es)")

    print("\nUso acumulado das personalidades:")
    for persona, qtd in contador_personalidades.items():
        print(f"- {persona}: {qtd} vez(es)")
    print("==============================\n")
        
def codigo_principal():
    personalidade_atual = "Formal"

    ultimas_interacoes = ler_ultimas_interacoes()
    
    if ultimas_interacoes:
        print("Últimas interações.","\n","=" * 50)
        for interacao in ultimas_interacoes:
            for linha in interacao:
                print(linha,end="")
        print("="*50+"\n")

    print("Bem-vindo ao ChatBot UFCA! Você pode digitar qualquer pergunta.\n")
    print("Para mudar a personalidade, use palavras como: engraçado, formal, rude.\nDigite sair para encerrar o programa")

    while True:
        duvida = input("Digite sua dúvida: ")
        if duvida.lower() == "sair":
            print("Chatbot: Até logo")
            mostrar_estatisticas()
            break

        #Detectar a mudança de personalidade 
        personalidade_atual, duvida_limpa = detectar_personalidade(duvida, personalidade_atual)

        #atualizar o contador de personalidades agora que indentificamos a que foi escolhida.
        contador_personalidades[personalidade_atual] += 1
        contador_personalidades_sessao[personalidade_atual] += 1

        #buscar resposta
        resposta = encontrar_respostas(duvida_limpa, personalidade_atual)

        print(f"({personalidade_atual}) Chatbot:", resposta)
        salvar_historico(duvida,resposta)

        # Salvar contador de personalidades no JSON
        with open(arquivo_qtd_personalidades, 'w', encoding='utf-8') as arq:
            json.dump(contador_personalidades, arq, ensure_ascii=False, indent=4)

#Chamar função principal

codigo_principal()