import streamlit as st
import pandas as pd
import plotly.express as px
from newsapi import NewsApiClient
from sympy.abc import lamda

from src.api.news_api import recuperar_noticias_financeiras
from src.service.finbert_analise_de_sentimento import analisar_sentimento
from src.service.otimizacao_de_porfolio import otimizar_portfolio


def gerar_interface() -> None:
    """ Cria a interface de usuário com Streamlit"""

    # Configuração da página
    st.set_page_config(page_title="Análise de Investimentos", layout="wide")

    if "aviso_aceito" not in st.session_state:
        st.session_state.aviso_aceito = False
    # Dialog de aviso - só mostra se não foi aceito ainda
    if not st.session_state.aviso_aceito:
        # Abre o diálogo
        @st.dialog("Aviso", width="large", on_dismiss=lambda: st.session_state.__setitem__("aviso_aceito", True))
        def mostrar_aviso():
            with open("./src/utils/aviso.md", "r", encoding="utf-8") as f:
                conteudo = f.read()
            st.write(conteudo)
        mostrar_aviso()

    st.title("Análise de Investimentos e Otimização de Portfólio")

    # Sidebar para entradas do usuário
    st.sidebar.header("Entradas do Usuário")
    acoes = st.sidebar.text_input("Lista de ações (separadas por vírgula)", "PETR4,CPLE3,BBAS3")
    anos_historico = st.sidebar.number_input("Anos históricos", min_value=1, max_value=20, value=3)
    metodo_otimizacao = st.sidebar.selectbox("Método de otimização", ["sharpe", "min_vol", "max_return"])
    aversao_ao_risco = st.sidebar.slider("Aversão ao risco (apenas para max_return)", min_value=0.1, max_value=2.0,
                                         value=1.0)

    # Botão para executar a análise
    if st.sidebar.button("Executar Análise"):
        st.session_state.aviso_aceito = True
        lista_acoes = [acao.strip() for acao in acoes.split(",")]

        # Verificação de entradas inválidas
        if not lista_acoes or any(len(acao) != 5 for acao in lista_acoes):
            st.warning(
                "Erro: Certifique-se de inserir códigos de ações válidos, separados por vírgulas (ex: PETR4,VALE3).")
        else:
            try:
                resultados_portfolio = otimizar_portfolio([f"{acao}.SA" for acao in lista_acoes], anos_historico,
                                                          metodo_otimizacao,
                                                          aversao_ao_risco)
                st.subheader("Resultados da Otimização do Portfólio")
                st.write(resultados_portfolio)
                # Gráfico de alocação ótima
                st.subheader("Alocação Ótima do Portfólio")
                df_alocacao = pd.DataFrame(list(resultados_portfolio["alocacao_otima"].items()),
                                           columns=["Ação", "Alocação"])
                fig_alocacao = px.pie(df_alocacao, values="Alocação", names="Ação", title="Alocação Ótima do Portfólio")
                st.plotly_chart(fig_alocacao)
                try:
                    # Análise de sentimento (exemplo com notícias fictícias)
                    noticias = recuperar_noticias_financeiras(st.secrets["newsapi"]["api_key"],
                                                              NewsApiClient.get_everything, lista_acoes)
                    resultados_sentimento = analisar_sentimento(noticias)

                    # Exibição dos resultados de sentimento
                    st.subheader("Análise de Sentimento das Notícias")
                    st.write(resultados_sentimento)

                    # Gráfico de sentimentos por ticker
                    st.subheader("Distribuição de Sentimentos por Ticker")
                    df_sentimento = pd.DataFrame(resultados_sentimento)
                    # Agrupa por Ticker e Sentimento, e conta a quantidade de notícias
                    df_contagem = df_sentimento.groupby(["Ticker", "Sentimento"]).size().reset_index(name="Quantidade")

                    # Cria o gráfico de barras agrupadas
                    fig_sentimento = px.bar(
                        df_contagem,
                        x="Ticker",
                        y="Quantidade",
                        color="Sentimento",
                        barmode="group",
                        title="Distribuição de Sentimentos por Ticker",
                        labels={"Quantidade": "Quantidade de Notícias", "Ticker": "Ticker"},
                        color_discrete_map={
                            "POSITIVE": "green",
                            "NEUTRAL": "gray",
                            "NEGATIVE": "red"
                        }
                    )
                    st.plotly_chart(fig_sentimento)

                    # Exibição de estatísticas
                    st.subheader("Estatísticas de Sentimentos e Portfólio")
                except ValueError as ve:
                    st.error(f"Erro de valor: {ve}")
                except KeyError as ke:
                    st.error(f"Erro de chave: {ke}")
                except Exception as e:
                    st.error(f"Erro inesperado: {e}")
            except Exception as e:
                st.error(f"Erro: Houve um erro ao otimizar o portfolio: {e}")
