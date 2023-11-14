import streamlit as st
from streamlit_extras.metric_cards import style_metric_cards
import pandas as pd
import numpy as np
import plotly.express as px

# Configurando a página
st.set_page_config('Dashboard Vendas', layout='wide')

# Carregando os dados e Transformando

dados = pd.read_excel('df_vendas_dashboard.xlsx')
dados['Faturamento'] = dados['Qtd Vendida'] * dados['Preço Unitario']
dados['Custo Total'] = dados['Qtd Vendida'] * dados['Custo Unitario']
dados['Ano'] = dados['Data da Venda'].dt.year
dados['Nome Mes'] = dados['Data da Venda'].dt.month_name()

# Titulo da página
st.title('Dashboard de Vendas')

# Construindo os filtros

with st.sidebar:
    st.markdown('# Filtros')
    st.write('Período')
    data_min = pd.to_datetime(st.date_input('Data Inicio', value= dados['Data da Venda'].min()))
    data_max = pd.to_datetime(st.date_input('Data Fim'))
    filtro_genero = st.multiselect('Genero do Cliente',dados['Genero'].unique(), default=dados['Genero'].unique())
    filtro_estado_civil = st.multiselect('Estado Civil do Cliente', dados['Estado Civil'].unique(),default=dados['Estado Civil'].unique())
    filtro_num_filhos = st.multiselect('Numero de filhos do Cliente', dados['Num Filhos'].unique(),default= dados['Num Filhos'].unique())
    filtro_nivel_escolar = st.multiselect('Nivel escolar do Cliente', dados['Nivel Escolar'].unique(),default= dados['Nivel Escolar'].unique())
    filtro_loja = st.multiselect('Loja', dados['Nome da Loja'].unique(),default= dados['Nome da Loja'].unique())
    filtro_tipo_loja = st.multiselect('Tipo Loja', dados['Tipo'].unique(),default= dados['Tipo'].unique())
    filtro_gerente = st.multiselect('Gerente da Loja', dados['Gerente Loja'].unique(),default= dados['Gerente Loja'].unique())
    filtro_produto = st.multiselect('Produto',dados['Produto'].unique(),default= dados['Produto'].unique())
    filtro_marca = st.multiselect('Marca',dados['Marca'].unique(),default= dados['Marca'].unique())
    filtro_tipo_produto = st.multiselect('Tipo do Produto',dados['Tipo do Produto'].unique(),default= dados['Tipo do Produto'].unique())

dados_filtrados = dados[
    dados['Data da Venda'].between(data_min, data_max)&
    dados['Genero'].isin(filtro_genero) &
    dados['Estado Civil'].isin(filtro_estado_civil) &
    dados['Num Filhos'].isin(filtro_num_filhos) &
    dados['Nivel Escolar'].isin(filtro_nivel_escolar) &
    dados['Nome da Loja'].isin(filtro_loja) &
    dados['Tipo'].isin(filtro_tipo_loja) &
    dados['Gerente Loja'].isin(filtro_gerente) &
    dados['Produto'].isin(filtro_produto) &
    dados['Marca'].isin(filtro_marca) &
    dados['Tipo do Produto'].isin(filtro_tipo_produto)
]

# Definindo Layout de 3 colunas

col1, col2, col3 = st.columns(3)

# Distribuindo as métricas


col1.metric('Total de Faturamento', dados_filtrados['Faturamento'].sum().round(2))
style_metric_cards()
col2.metric('Volume Total', dados_filtrados['Qtd Vendida'].sum())
style_metric_cards()
col3.metric('Melhor Mês', dados_filtrados.groupby(['Ano','Nome Mes']).sum('Faturamento').reset_index().loc[1,'Nome Mes'])
style_metric_cards()

# Distribuindo os gráficos
with col1:
    vendas_por_loja = dados_filtrados.groupby(['Nome da Loja']).sum('Faturamento').reset_index().sort_values(by = 'Faturamento')
    fig_vendas_por_loja = px.bar(data_frame=vendas_por_loja, x = 'Faturamento', y = 'Nome da Loja', title='Faturamento por Loja')
    st.plotly_chart(fig_vendas_por_loja, use_container_width=True)
    
with col2:
    vendas_por_produto = dados_filtrados.groupby(['Produto']).sum('Faturamento').reset_index().sort_values(by = 'Faturamento')
    fig_vendas_por_produto = px.bar(data_frame=vendas_por_produto, x = 'Faturamento', y = 'Produto', title='Faturamento por Produto' )
    st.plotly_chart(fig_vendas_por_produto, use_container_width=True)

with col3:
    vendas_por_marca = dados_filtrados.groupby(['Marca']).sum('Faturamento').reset_index().sort_values(by = 'Faturamento')
    fig_vendas_por_marca = px.bar(data_frame=vendas_por_marca, x = 'Faturamento', y = 'Marca', title='Faturamento por Marca')
    st.plotly_chart(fig_vendas_por_marca, use_container_width=True)

vendas_por_mes = dados_filtrados.groupby(['Data da Venda']).sum('Faturamento').reset_index()
fig_vendas_por_mes = px.line(data_frame=vendas_por_mes, x = 'Data da Venda', y = 'Faturamento', title='Faturamento mensal')
st.plotly_chart(fig_vendas_por_mes, use_container_width=True)





