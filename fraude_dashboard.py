import streamlit as st
from pymongo import MongoClient
import pandas as pd
import plotly.express as px

# Configuração do MongoDB
MONGO_URI = "mongodb://admin:admin@localhost:27017/"
mongo_client = MongoClient(MONGO_URI)
mongo_db = mongo_client["kafka_fraudes_v2"]
fraudes_collection = mongo_db["transacoes_suspeitas"]

import streamlit as st

# Ajusta a página para ocupar toda a largura da tela
st.set_page_config(
    page_title="Painel de Detecção de Fraudes",
    page_icon="🕵️",
    layout="wide"  
)

# Adicionar título e descrição
st.title("🕵️ Painel de Detecção de Fraudes em Tempo Real")

st.markdown(
    """
    Bem-vindo ao **Painel de Detecção de Fraudes em Tempo Real**!  
    Este painel apresenta um monitoramento contínuo das transações financeiras, identificando **possíveis fraudes** 
    com base em **regras predefinidas**. As regras aplicadas são:

    - **Alta Frequência** 🔄 → Usuário realizou múltiplas transações em menos de 5 minutos.
    - **Alto Valor** 💰 → Transação superior ao dobro do maior valor já gasto pelo usuário.
    - **Outro País** ✈️ → Transação realizada em um país diferente dentro de um intervalo de 2 horas.

    As fraudes detectadas são exibidas abaixo, permitindo a análise de padrões e tendências.
    """
)

# Carregar dados do MongoDB para um DataFrame do Pandas
def carregar_dados():
    cursor = fraudes_collection.find({})
    data = list(cursor)
    if data:
        df = pd.DataFrame(data)
        
        # Separar os campos da localização
        df["Cidade"] = df["location"].apply(lambda x: x.get("city", "Desconhecido") if isinstance(x, dict) else "Desconhecido")
        df["Estado"] = df["location"].apply(lambda x: x.get("state", "Desconhecido") if isinstance(x, dict) else "Desconhecido")
        df["País"] = df["location"].apply(lambda x: x.get("country", "Desconhecido") if isinstance(x, dict) else "Desconhecido")
        
        # Converter timestamp para formato legível
        df["Data e Hora"] = pd.to_datetime(df["timestamp"], unit="s")
        
        # Traduzindo nomes das colunas
        df.rename(columns={
            "_id": "ID",
            "user_id": "Usuário",
            "card_id": "Cartão",
            "value": "Valor da Transação",
            "rule_detected": "Regra Detectada",
            "site_id": "ID do Estabelecimento",
            "merchant_category": "Categoria do Comércio"
        }, inplace=True)
        
        return df
    return pd.DataFrame()

df = carregar_dados()

# Se houver dados, exibir os insights
if not df.empty:
    # Filtro por Data
    st.sidebar.header("📅 Filtrar por Data")
    start_date = st.sidebar.date_input("Data Inicial", df["Data e Hora"].min().date())
    end_date = st.sidebar.date_input("Data Final", df["Data e Hora"].max().date())
    df_filtered = df[(df["Data e Hora"].dt.date >= start_date) & (df["Data e Hora"].dt.date <= end_date)]

    # Exibir tabela com fraudes filtradas
    st.subheader("📜 Tabela de Fraudes Detectadas")
    st.dataframe(df_filtered[["Data e Hora", "Usuário", "Cartão", "Valor da Transação", "Cidade", "Estado", "País", "Regra Detectada", "Categoria do Comércio"]])

    # Gráfico 1: País com mais fraudes
    st.subheader("🌎 Países com Mais Fraudes")
    df_pais = df_filtered["País"].value_counts().reset_index()
    df_pais.columns = ["País", "Quantidade"]
    fig_pais = px.bar(df_pais, x="País", y="Quantidade", title="Fraudes por País", color="Quantidade")
    st.plotly_chart(fig_pais)

    # Gráfico 2: Fraudes por Hora do Dia (Faixas de Horário)
    st.subheader("⏳ Fraudes por Faixa de Horário")
    df_filtered["Hora"] = df_filtered["Data e Hora"].dt.hour
    df_horas = df_filtered.groupby("Hora").size().reset_index(name="Quantidade")
    fig_horas = px.line(df_horas, x="Hora", y="Quantidade", markers=True, title="Média de Fraudes por Horário do Dia")
    st.plotly_chart(fig_horas)

    # Gráfico 3: Regras de Fraude Mais Violadas
    st.subheader("⚠️ Regras de Fraude Mais Comuns")
    df_regras = df_filtered["Regra Detectada"].explode().value_counts().reset_index()
    df_regras.columns = ["Regra", "Quantidade"]
    fig_regras = px.pie(df_regras, names="Regra", values="Quantidade", title="Distribuição das Regras de Fraude")
    st.plotly_chart(fig_regras)

    # Gráfico 4: Usuário Mais Fraudulento
    st.subheader("🕵️‍♂️ Usuário Mais Fraudulento")
    df_users = df_filtered["Usuário"].value_counts().reset_index()
    df_users.columns = ["Usuário", "Quantidade"]
    st.table(df_users.head(10))

else:
    st.warning("⚠️ Nenhum dado de fraude encontrado. Aguarde ou gere novas transações.")

