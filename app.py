import streamlit as st
import json
import os
from datetime import datetime
from core.chatbot import ChatBot
from core.estatisticas import Estatisticas
from core.relatorio import gerar_relatorio_final

# --- Funções de Apoio ---
@st.cache_resource
def carregar_bot():
    with open("data/json_chatbot.json", "r", encoding="utf-8") as arq:
        base_conhecimento = json.load(arq)
    bot = ChatBot(base_conhecimento)
    return bot

@st.cache_data
def carregar_perguntas_e_categorias():
    with open("data/json_chatbot.json", "r", encoding="utf-8") as arq:
        base_conhecimento = json.load(arq)
    perguntas = [item["pergunta"] for item in base_conhecimento["Formal"]]
    mapeamento_categorias = {
        "Sobre a UFCA": ["ufca", "história", "missão", "pública", "cidades"],
        "Vida Acadêmica": ["ingressar", "sigaa", "notas", "trancamento", "matrícula", "horas complementares", "prova final", "carteirinha", "intercâmbio", "coordenador", "falta"],
        "Locais e Horários": ["biblioteca", "horário", "secretaria", "laboratórios", "auditório", "xerox", "cópias"],
        "Assistência Estudantil": ["restaurante", "moradia", "prae", "auxílios", "psicológico", "deficiência", "transporte"],
        "Outros": ["wi-fi", "eduroam", "eventos", "intercampi", "quadras", "achados e perdidos"]
    }
    categorias = {cat: [] for cat in mapeamento_categorias.keys()}
    for pergunta in perguntas:
        categorizada = False
        for cat, keywords in mapeamento_categorias.items():
            if any(kw in pergunta.lower() for kw in keywords):
                categorias[cat].append(pergunta); categorizada = True; break
        if not categorizada:
            if "Outros" not in categorias: categorias["Outros"] = []
            categorias["Outros"].append(pergunta)
    return categorias

# --- Inicialização ---
bot = carregar_bot()
categorias = carregar_perguntas_e_categorias()

if "messages" not in st.session_state:
    # ## <-- ALTERAÇÃO: Histórico agora é salvo em uma variável separada
    st.session_state.historical_messages = []
    ultimas_interacoes_raw = bot.historico.ler_ultimas_interacoes(n=5)
    if ultimas_interacoes_raw:
        for interacao in ultimas_interacoes_raw:
            pergunta_raw = interacao[0].replace("Usuário: ", "").strip()
            resposta_raw = interacao[1].replace("Chatbot: ", "").strip()
            st.session_state.historical_messages.append({"role": "user", "content": pergunta_raw})
            st.session_state.historical_messages.append({"role": "assistant", "content": resposta_raw})

    # A conversa atual começa sempre limpa
    st.session_state.messages = [{"role": "assistant", "content": "Olá! Escolha uma personalidade e sua pergunta."}]
    
    st.session_state.waiting_for_suggestion = False
    st.session_state.question_to_learn = ""
    st.session_state.show_toast = False
    estatisticas_gerais = Estatisticas(None, None, None, bot.base_conhecimento, bot.historico.arquivo)
    st.session_state.sugestoes = estatisticas_gerais.obter_sugestoes_perguntas()


# --- Interface Principal ---
st.set_page_config(page_title="Campus Core", page_icon="🤖")

if st.session_state.get("show_toast"):
    st.toast(":green[Resposta recebida!]", icon="✅")
    st.session_state.show_toast = False

st.title("🤖 Campus Core - Chatbot da UFCA")
st.caption("Selecione uma personalidade na barra lateral, escolha um tópico e faça sua pergunta.")

# ## <-- NOVA SEÇÃO: Expander para o histórico antigo
if st.session_state.historical_messages:
    with st.expander("Visualizar últimas 5 interações do histórico"):
        for message in st.session_state.historical_messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        st.info("Esta é uma visualização estática do seu histórico anterior.")


if st.session_state.sugestoes:
    st.subheader("💡 Sugestões (Perguntas Mais Frequentes)")
    cols = st.columns(len(st.session_state.sugestoes))
    for i, pergunta_sugerida in enumerate(st.session_state.sugestoes):
        with cols[i]:
            if st.button(pergunta_sugerida, key=f"sug_{pergunta_sugerida}", use_container_width=True):
                resposta = bot.encontrar_resposta_predefinida(pergunta_sugerida)
                st.session_state.show_toast = True
                st.session_state.messages.append({"role": "user", "content": pergunta_sugerida})
                st.session_state.messages.append({"role": "assistant", "content": resposta})
                bot.historico.salvar(pergunta_sugerida, resposta)
                st.rerun()
    st.divider()

st.subheader("Selecione sua Pergunta")

# (O resto do arquivo permanece o mesmo)
for categoria, perguntas in categorias.items():
    with st.expander(f"**{categoria}**"):
        for pergunta in perguntas:
            if st.button(pergunta, key=f"pre_{pergunta}", use_container_width=True):
                resposta = bot.encontrar_resposta_predefinida(pergunta)
                st.session_state.show_toast = True
                st.session_state.messages.append({"role": "user", "content": pergunta})
                st.session_state.messages.append({"role": "assistant", "content": resposta})
                bot.historico.salvar(pergunta, resposta)
                st.rerun()

with st.expander("**Perguntas Aprendidas (memória do bot)**"):
    bot.aprendizado.dados = bot.aprendizado._carregar()
    if not bot.aprendizado.dados:
        st.info("O bot ainda não aprendeu nenhuma pergunta nova.")
    for item in bot.aprendizado.dados:
        pergunta_aprendida = item["pergunta"]
        if st.button(pergunta_aprendida, key=f"apr_{pergunta_aprendida}", use_container_width=True):
            resposta = bot.processar_pergunta_customizada(pergunta_aprendida)
            st.session_state.show_toast = True
            st.session_state.messages.append({"role": "user", "content": pergunta_aprendida})
            st.session_state.messages.append({"role": "assistant", "content": resposta})
            bot.historico.salvar(pergunta_aprendida, resposta)
            st.rerun()

with st.expander("**Outra Pergunta (Não encontrou sua dúvida?)**"):
    pergunta_customizada = st.text_input("Digite sua pergunta aqui:")
    if st.button("Enviar Pergunta", key="send_custom"):
        if pergunta_customizada:
            resposta = bot.processar_pergunta_customizada(pergunta_customizada)
            st.toast("Pergunta processada!", icon="🤖")
            st.session_state.messages.append({"role": "user", "content": pergunta_customizada})
            if resposta is None:
                st.session_state.messages.append({"role": "assistant", "content": "Não sei a resposta para isso. Pode me ajudar a aprender?"})
                st.session_state.waiting_for_suggestion = True
                st.session_state.question_to_learn = pergunta_customizada
            else:
                st.session_state.messages.append({"role": "assistant", "content": resposta})
                bot.historico.salvar(pergunta_customizada, resposta)
            st.rerun()

if st.session_state.waiting_for_suggestion:
    sugestao_resposta = st.text_input("Qual seria uma boa resposta para a pergunta acima?")
    if st.button("Enviar Sugestão", key="send_suggestion"):
        bot.aprendizado.salvar_novo_conhecimento(st.session_state.question_to_learn, sugestao_resposta)
        agradecimento = "Obrigado! Aprendi algo novo com sua ajuda."
        st.toast("Sugestão aprendida com sucesso!", icon="🧠")
        st.session_state.messages.append({"role": "assistant", "content": agradecimento})
        bot.historico.salvar(f"(Aprendendo): {st.session_state.question_to_learn}", f"(Sugestão): {sugestao_resposta}")
        st.session_state.waiting_for_suggestion = False
        st.session_state.question_to_learn = ""
        st.rerun()

st.subheader("Histórico da Conversa")
with st.container(border=True):
    # Este container agora mostra apenas as mensagens da sessão ATUAL
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

with st.sidebar:
    st.header("Opções da Sessão")
    st.subheader("1. Escolha a Personalidade")
    personalidade_escolhida = st.radio( "Com quem você quer falar?", ["Formal", "Engracado", "Rude"], label_visibility="collapsed")
    if "personalidade_atual" not in st.session_state or st.session_state.personalidade_atual != personalidade_escolhida:
        bot.personalidade.definir_personalidade_atual(personalidade_escolhida)
        st.session_state.personalidade_atual = personalidade_escolhida
        if "messages" in st.session_state and len(st.session_state.messages) > 1:
             st.toast(f"Personalidade alterada para {personalidade_escolhida}!")

    st.divider()
    if st.button("Encerrar Sessão e Gerar Relatório"):
        estatisticas = Estatisticas(
            perguntas_chaves_sessao=bot.perguntas_chaves_sessao,
            contador_sessao=bot.personalidade.contador_sessao,
            contador_acumulado=bot.personalidade.contador,
            base_conhecimento=bot.base_conhecimento,
            historico_path=bot.historico.arquivo
        )
        caminho_relatorio = gerar_relatorio_final(estatisticas)
        if caminho_relatorio and os.path.exists(caminho_relatorio):
            st.success(f"Relatório '{os.path.basename(caminho_relatorio)}' gerado!")
            with open(caminho_relatorio, "rb") as file:
                st.download_button("Baixar Novo Relatório", file, os.path.basename(caminho_relatorio), "text/plain")
        else:
            st.error("Falha ao gerar o relatório.")
            
    if st.button("Iniciar Nova Sessão"):
        st.session_state.clear()
        st.rerun()
    st.divider()
    st.header("Relatórios Salvos")
    diretorio_relatorios = "relatorios"
    if os.path.exists(diretorio_relatorios) and os.listdir(diretorio_relatorios):
        arquivos = sorted(
            os.listdir(diretorio_relatorios),
            key=lambda f: os.path.getmtime(os.path.join(diretorio_relatorios, f)),
            reverse=True
        )
        for nome_arquivo in arquivos:
            caminho_completo = os.path.join(diretorio_relatorios, nome_arquivo)
            with open(caminho_completo, "rb") as file:
                st.download_button(
                    label=f"📄 {nome_arquivo}",
                    data=file,
                    file_name=nome_arquivo,
                    mime="text/plain",
                    key=f"dl_{nome_arquivo}"
                )
    else:
        st.info("Nenhum relatório foi gerado ainda.")