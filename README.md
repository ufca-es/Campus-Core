# 🤖 Campus Core - Chatbot da UFCA

![Streamlit](https://img.shields.io/badge/Streamlit-1.49.1-FF4B4B?style=for-the-badge&logo=streamlit)
![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python)
![Status](https://img.shields.io/badge/Status-Concluído-28a745?style=for-the-badge)

O **Campus Core** é um chatbot interativo desenvolvido como projeto final para a disciplina de **Fundamentos de Programação** da **Universidade Federal do Cariri (UFCA)**. O objetivo é auxiliar estudantes e visitantes, respondendo às perguntas mais comuns sobre a vida acadêmica, serviços e infraestrutura da universidade de forma rápida e intuitiva.

A principal característica do chatbot é a sua capacidade de responder em três personalidades distintas, permitindo que o usuário escolha o tom da conversa.

---

## ✨ Funcionalidades

* **Múltiplas Personalidades:** Converse com o bot em modo **Formal** (🔵), **Engraçado** (🟢) ou **Rude** (🔴), cada um com um avatar e estilo de resposta únicos.
* **Interface Gráfica Interativa:** Uma interface moderna e responsiva criada com Streamlit, com layout em duas colunas para facilitar a navegação e visualização.
* **Busca em Tempo Real:** Encontre perguntas rapidamente com uma barra de busca que filtra os resultados a cada tecla digitada.
* **Modo de Aprendizagem:** Se o bot não souber uma resposta, você pode ensiná-lo! As novas perguntas e respostas são salvas e ficam disponíveis para todos.
* **Histórico e Relatórios:** Acompanhe o histórico da sua conversa e gere relatórios detalhados da sessão, com estatísticas de uso e perguntas mais frequentes.
* **Sugestões Inteligentes:** O bot sugere as perguntas mais populares com base no histórico de uso de todos os usuários.
* **Tema Customizado:** Um tema visual escuro e coeso para uma experiência de uso mais agradável.

---

## 🚀 Como Executar

Siga os passos abaixo para rodar o projeto em sua máquina local.

### Pré-requisitos
* Python (versão 3.8 ou superior)

### Passos de Instalação

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/seu-usuario/Campus-Core.git](https://github.com/seu-usuario/Campus-Core.git)
    cd Campus-Core
    ```

2.  **Crie e ative um ambiente virtual:**
    ```bash
    # Windows
    python -m venv venv
    .\venv\Scripts\activate

    # Linux / macOS
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Crie a pasta de assets para os ícones:**
    * Na raiz do projeto, crie uma pasta chamada `assets`.
    * Dentro dela, adicione os ícones: `avatar_formal.png` (fundo azul), `avatar_engracado.png` (fundo verde) e `avatar_rude.png` (fundo vermelho).

5.  **Execute a aplicação:**
    ```bash
    streamlit run app.py
    ```
O aplicativo será aberto automaticamente no seu navegador.

---

## 🖼️ Demonstrações

### Interface Principal
A interface é dividida em duas colunas para facilitar o uso: à esquerda, os controles e perguntas; à direita, o histórico da conversa.

![Interface Principal](/assets/screenshot1.png)

### Busca em Tempo Real e Modo Ativo
A barra de busca filtra as perguntas instantaneamente. O indicador de "Modo Ativo" mostra a personalidade atual com a cor correspondente.

![Busca e Modo Ativo](/assets/screenshot2.png)

### Exemplo de Conversa
As respostas e os ícones do bot mudam de cor de acordo com a personalidade selecionada. O ícone do usuário agora aparece corretamente.

![Exemplo de Conversa](/assets/screenshot3.png)

### Barra Lateral com Relatórios
A barra lateral oferece acesso rápido às opções da sessão e à lista de relatórios salvos para download.

![Barra Lateral](/assets/screenshot4.png)

---

## 👥 Equipe

Este projeto foi desenvolvido pelos seguintes integrantes, como requisito da disciplina de Fundamentos de Programação (ES0003).


* **Paulo Gabriel:** Arquiteto do Core (Backend)
* **Ângelo Gabriel:** Designer de Interface (Frontend)
* **José Luiz:** Engenheiro de Conteúdo (Dados)
* **Jetro Viana:** Gerente de Projeto e Documentação (DevOps/QA)

### Mentor
* **Prof. Dr. Williamson Silva**