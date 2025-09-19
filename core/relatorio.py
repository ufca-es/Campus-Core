"""Módulo responsável por gerar relatórios de uso do chatbot."""

import os
from datetime import datetime
from .estatisticas import Estatisticas

def gerar_relatorio_final(dados_estatisticos: Estatisticas, diretorio="relatorios"):
    """
    Gera um relatório de texto contendo estatísticas da sessão atual.

    O arquivo é salvo no diretório especificado e possui nome único
    com base na data e hora de geração.

    Args:
        dados_estatisticos (Estatisticas): Objeto com dados da sessão.
        diretorio (str): Caminho do diretório onde salvar o relatório.

    Returns:
        str | None: Caminho do arquivo gerado ou None em caso de erro.
    """
    try:
        os.makedirs(diretorio, exist_ok=True)
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        nome_arquivo = f"relatorio_chatbot_{timestamp}.txt"
        caminho_completo = os.path.join(diretorio, nome_arquivo)

        print(f"Gerando relatório final em: {caminho_completo}")

        with open(caminho_completo, "w", encoding="utf-8") as f:
            f.write("=" * 50 + "\n")
            f.write(" RELATÓRIO DE SESSÃO DO CHATBOT UFCA\n")
            f.write(f" Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
            f.write("=" * 50 + "\n\n")

            total_interacoes = len(dados_estatisticos.perguntas_chaves_sessao)
            f.write(f"Total de interações na sessão: {total_interacoes}\n")

            if dados_estatisticos.perguntas_chaves_sessao:
                from collections import Counter
                contador = Counter(dados_estatisticos.perguntas_chaves_sessao)
                if contador:
                    pergunta_mais_frequente, vezes = contador.most_common(1)[0]
                    f.write(f"Pergunta mais feita: '{pergunta_mais_frequente}' ({vezes} vezes)\n\n")
            
            f.write("Uso das personalidades nesta sessão:\n")
            for persona, qtd in dados_estatisticos.contador_sessao.items():
                f.write(f"- {persona}: {qtd} vez(es)\n")
            
            f.write("\nUso acumulado (total) das personalidades:\n")
            for persona, qtd in dados_estatisticos.contador_acumulado.items():
                f.write(f"- {persona}: {qtd} vez(es)\n")
            
            f.write("\n" + "=" * 50 + "\n")
            f.write("FIM DO RELATÓRIO\n")
            
        print("Relatório gerado com sucesso!")
        return caminho_completo

    except Exception as e:
        print(f"ERRO: Não foi possível gerar o relatório. Causa: {e}")
        return None
