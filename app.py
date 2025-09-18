import streamlit as st
import json
from core.chatbot import ChatBot
from core.personalidade import detectar_personalidade

# --- Configuração da Página e Carregamento do Bot ---

# Define o título e o ícone que aparecerão na aba do navegador
st.set_page_config(page_title="Campus Core", page_icon="🤖")

# Título principal da página
st.title("🤖 Campus Core - Chatbot da UFCA")
st.caption("Faça perguntas sobre a UFCA ou mude minha personalidade com 'rude', 'engraçado' ou 'formal'.")

# Função para carregar o bot (com cache para não recarregar a cada interação)
@st.cache_resource
def carregar_bot():
    """ Carrega a base de conhecimento e inicializa o chatbot. """
    with open("data/json_chatbot.json", "r", encoding="utf-8") as arq:
        base_conhecimento = json.load(arq)
    bot = ChatBot(base_conhecimento)
    return bot

# Carrega o bot na primeira vez que o script é executado
bot = carregar_bot()

# --- Gerenciamento do Histórico da Conversa ---

# Inicializa o histórico do chat na sessão se ele não existir
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Adiciona uma mensagem inicial do bot
    st.session_state.messages.append(
        {"role": "assistant", "content": "Olá! Sou o Campus Core. Como posso te ajudar hoje?"}
    )

# Exibe todas as mensagens do histórico na tela
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Lógica de Interação ---

# Cria o campo de texto para o usuário digitar, no rodapé da página
if prompt := st.chat_input("Digite sua dúvida..."):
    # Adiciona e exibe a mensagem do usuário na tela
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Processa a mensagem para obter a resposta do bot
    with st.chat_message("assistant"):
        # Reutiliza a mesma lógica de detecção de personalidade do seu código original
        nova_personalidade, pergunta_limpa = detectar_personalidade(prompt, bot.personalidade.atual)
        
        # Se a personalidade mudou...
        if nova_personalidade != bot.personalidade.atual:
            bot.personalidade.alterar(nova_personalidade)
            bot.personalidade.salvar_contador()
            # Se era só um comando para mudar, responde confirmando
            if not pergunta_limpa.strip():
                resposta = f"Personalidade alterada para {bot.personalidade.atual}. Como posso ajudar?"
            # Se tinha uma pergunta junto, avisa da mudança e responde
            else:
                st.info(f"Personalidade alterada para {bot.personalidade.atual}.")
                resposta = bot.encontrar_resposta(pergunta_limpa)
        # Se a personalidade não mudou, apenas responde a pergunta
        else:
            resposta = bot.encontrar_resposta(pergunta_limpa)
        
        # Salva a interação no arquivo de log (opcional, mas bom manter)
        bot.historico.salvar(prompt, resposta)
        
        # Exibe a resposta do bot
        st.markdown(resposta)

    # Adiciona a resposta do bot ao histórico da sessão para que ela não suma
    st.session_state.messages.append({"role": "assistant", "content": resposta})