import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_dynamic_filters import DynamicFilters

#Configurações iniciais da página
st.set_page_config(
    page_title="Vendas Dashboard",
    page_icon=":bar_chart",
    layout="wide"
)

#Carregando arquivo xlsx e formatando datas
df = pd.read_excel("supermarkt_sales.xlsx")
df["Hour"] = pd.to_datetime(df["Time"], format="%H:%M:%S").dt.hour

#Sidebar Título e Filtros
st.sidebar.header("Selecione seus filtros aqui: ")
dynamic_filters = DynamicFilters(df=df, filters=['City', 'Customer_type', 'Gender', 'Payment'], )
dynamic_filters.display_filters(location='sidebar')

#Dataframe Filtrado
df_selecao = dynamic_filters.filter_df(except_filter=None)

#Página Principal
st.title(':bar_chart: Dashboard de Vendas') #Título

#Cálculos Big Numbers
vendas_totais = int(df_selecao['Total'].sum())
vendas_medias = round(df_selecao['Total'].mean(),2)
avaliacao_media = round(df_selecao['Rating'].mean(),1)
avaliacao_estrelas = ":star:" * int(avaliacao_media)

#Posicionamento Big Numbers
coluna_esquerda, coluna_meio, coluna_direita = st.columns(3)
with coluna_esquerda:
    st.subheader("Vendas Totais")
    st.subheader(f"US ${vendas_totais:,}")
with coluna_meio:
    st.subheader("Vendas Médias")
    st.subheader(f"US ${vendas_medias:,}")
with coluna_direita:
    st.subheader("Avaliação Média")
    st.subheader(avaliacao_estrelas)
    st.subheader(f"{avaliacao_media}")


st.markdown("---")

df_vendas_por_linha_de_produto = (
    df_selecao.groupby('Product line').sum()[['Total']].sort_values('Total')
)


fig_df_vendas_por_linha_de_produto = px.bar(
    df_vendas_por_linha_de_produto,
    x = 'Total',
    y = df_vendas_por_linha_de_produto.index,
    orientation='h',
    title='Vendas por Linha de Produto'
)

df_vendas_por_hora = df_selecao.groupby('Hour').sum()[['Total']]

fig_vendas_por_hora = px.line(
    df_vendas_por_hora,
    y = 'Total',
    x = df_vendas_por_hora.index,
    title = 'Vendas por Hora'

)

df_lucro_por_linha_de_produto = (
    df_selecao.groupby('Product line').sum()[['gross income']].sort_values('gross income')
)


fig_df_lucro_por_linha_de_produto = px.bar(
    df_lucro_por_linha_de_produto,
    x = 'gross income',
    y = df_lucro_por_linha_de_produto.index,
    orientation='h',
    title='Lucro por Linha de Produto'
)

df_vendas_por_genero = df_selecao.groupby('Gender').sum()[['Total']]

fig_vendas_por_genero = px.pie(
    df_vendas_por_genero,
    names= df_vendas_por_genero.index,
    values='Total',
    title='Vendas por Gênero'
)

coluna_grafico_esquerda, coluna_grafico_direita = st.columns(2)
with coluna_grafico_esquerda:
    coluna_grafico_esquerda.plotly_chart(fig_df_vendas_por_linha_de_produto, use_container_width=True)
    coluna_grafico_esquerda.plotly_chart(fig_df_lucro_por_linha_de_produto, use_container_width=True)
with coluna_grafico_direita:
    coluna_grafico_direita.plotly_chart(fig_vendas_por_hora, use_container_width=True)
    coluna_grafico_direita.plotly_chart(fig_vendas_por_genero, use_container_width=True)

st.dataframe(df_selecao)