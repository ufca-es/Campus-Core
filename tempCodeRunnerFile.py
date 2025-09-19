import json
from core.chatbot import ChatBot

if __name__ == "__main__":
    with open("data/json_chatbot.json", "r", encoding="utf-8") as arq:
        base_conhecimento = json.load(arq)

    bot = ChatBot(base_conhecimento)
    bot.iniciar()