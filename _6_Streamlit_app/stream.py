import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime
from io import StringIO
import base64
import requests

# Configuração inicial
st.set_page_config(layout="wide", page_title="Análise de Comercialização")

# Opção 1: Melhor solução para GitHub (URL raw - recomendada)
@st.cache_data
def carregar_dados():
    try:
        # Opção 1: Carregar do GitHub (URL raw)
        url = "https://raw.githubusercontent.com/Gabriel-2040/Projeto_Unidade_3/main/_6_Streamlit/assets/dados_completos.csv"
        df = pd.read_csv(url)
        
        # Opção 2 alternativa (local) - descomente se necessário:
        # df = pd.read_csv(r'E:\digital college\DA18\PYTHON\Projeto_Unidade_3\_5_Dataframes_tratados\dados_completos.csv')
        
        # Processamento dos dados (APÓS carregamento)
        # Criar coluna data corretamente
        df['data'] = pd.to_datetime(df['ano_mes'].astype(str), format='%Y%m')
        df['ano'] = df['data'].dt.year
        df['mes'] = df['data'].dt.month

        # Verificar se há datas inválidas
        if df['data'].isnull().any():
            st.warning("Algumas datas não puderam ser convertidas corretamente")
        
        return df[['estado', 'prod_und', 'tipo_de_comercializacao', 'valor', 'ano', 'mes', 'data', 'macrogrupo']]
    
    except Exception as e:
        st.error(f"Erro ao carregar ou processar dados: {e}")
        return None
    
    # except FileNotFoundError:
    #     st.error("Arquivo de dados não encontrado. Verifique o caminho.")
    #     return pd.DataFrame()  # Retorna DataFrame vazio para evitar erros

# Carregar dados
df = carregar_dados()

# Verificar se os dados foram carregados
if df.empty:
    st.stop()  # Para a execução se não houver dados

# Sidebar - Filtros
st.sidebar.header('Filtros')
anos = st.sidebar.multiselect('Anos', options=sorted(df['ano'].unique()), default=sorted(df['ano'].unique()))
mes = st.sidebar.multiselect('Meses', options=sorted(df['mes'].unique()), default=sorted(df['mes'].unique()))
estados = st.sidebar.multiselect('Estados', options=sorted(df['estado'].unique()), default=sorted(df['estado'].unique()))
tipo_comerc = st.sidebar.multiselect('Tipo Comercialização', 
                                   options=sorted(df['tipo_de_comercializacao'].unique()), 
                                   default=sorted(df['tipo_de_comercializacao'].unique()))

# Aplicar filtros
df_filtrado = df[
    (df['ano'].isin(anos)) & 
    (df['mes'].isin(mes)) &
    (df['estado'].isin(estados)) & 
    (df['tipo_de_comercializacao'].isin(tipo_comerc))
]

# Página principal
st.title('Análise de Comercialização de Produtos')

# Abas
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Visão Geral", 
    "Varejo vs Atacado vs Produtor", 
    "Instabilidade de Preços", 
    "Sazonalidade", 
    "Variação por Período"
])

with tab1:
    st.header("Visão Geral do Faturamento")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Faturamento por estado
        fat_estado = df_filtrado.groupby('estado')['valor'].sum().sort_values(ascending=False)
        st.subheader("Faturamento por Estado")
        fig, ax = plt.subplots(figsize=(10, 6))  # Aumentei a altura para melhor visualização
        fat_estado.plot(kind='bar', ax=ax)
        plt.xticks(rotation=45)  # Rotacionar rótulos para melhor legibilidade
        st.pyplot(fig)
        
    with col2:
        # Faturamento por ano
        st.subheader("Faturamento por Ano")
        fat_ano = df_filtrado.groupby('ano')['valor'].sum()
        fig, ax = plt.subplots(figsize=(10, 6))
        fat_ano.plot(kind='line', marker='o', ax=ax)
        st.pyplot(fig)
    
    # Top produtos
    st.subheader("Top 5 Produtos")
    top_prod = df_filtrado.groupby('prod_und')['valor'].sum().nlargest(5)
    fig, ax = plt.subplots(figsize=(10, 6))
    top_prod.plot(kind='bar', ax=ax)
    plt.xticks(rotation=45)
    st.pyplot(fig)

with tab2:
    st.header("Comparação Varejo x Atacado x Produtor")
    
    # Comparação por tipo de comercialização
    comp_tipo = df_filtrado.groupby('tipo_de_comercializacao')['valor'].agg(['sum', 'mean', 'count'])
    st.dataframe(comp_tipo.style.format("{:,.2f}"))
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Faturamento por Tipo")
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.boxplot(data=df_filtrado, x='tipo_de_comercializacao', y='valor', ax=ax)
        plt.xticks(rotation=45)
        st.pyplot(fig)
    
    with col2:
        st.subheader("Distribuição por Estado")
        pivot = pd.pivot_table(df_filtrado, values='valor', index='estado', 
                              columns='tipo_de_comercializacao', aggfunc='sum')
        fig, ax = plt.subplots(figsize=(12, 8))  # Ajuste de tamanho
        pivot.plot(kind='bar', stacked=True, ax=ax)
        plt.xticks(rotation=45)
        plt.legend(title='Tipo Comercialização')
        st.pyplot(fig)

with tab3:
    st.header("Instabilidade de Preços por Estado")
    
    # Calcular coeficiente de variação
    cv_estado = df_filtrado.groupby('estado')['valor'].agg(['mean', 'std'])
    cv_estado['cv'] = (cv_estado['std'] / cv_estado['mean']) * 100
    cv_estado = cv_estado.sort_values('cv', ascending=False)
    
    st.subheader("Estados com Maior Instabilidade")
    st.dataframe(cv_estado.style.format("{:,.2f}"))
    
    # Boxplot por estado
    st.subheader("Distribuição de Preços por Estado")
    fig, ax = plt.subplots(figsize=(14, 8))  # Ajuste de tamanho
    sns.boxplot(data=df_filtrado, x='estado', y='valor', ax=ax)
    plt.xticks(rotation=45)
    st.pyplot(fig)

with tab4:
    st.header("Análise de Sazonalidade")
    
    produto_selecionado = st.selectbox("Selecione um produto", df_filtrado['prod_und'].unique())
    
    # Dados do produto selecionado
    df_produto = df_filtrado[df_filtrado['prod_und'] == produto_selecionado]
    
    if not df_produto.empty:
        # Sazonalidade por mês
        sazonal = df_produto.groupby(['ano', 'mes'])['valor'].sum().unstack(level=0)
        
        st.subheader(f"Sazonalidade para {produto_selecionado}")
        fig, ax = plt.subplots(figsize=(12, 8))  # Ajuste de tamanho
        sazonal.plot(ax=ax)
        plt.legend(title='Ano', bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()
        st.pyplot(fig)
        
        # Meses sem venda
        meses_sem_venda = sazonal[sazonal.isnull().any(axis=1)]
        if not meses_sem_venda.empty:
            st.warning(f"Meses sem vendas para {produto_selecionado}: {list(meses_sem_venda.index)}")
    else:
        st.warning("Nenhum dado disponível para o produto selecionado com os filtros atuais")

with tab5:
    st.header("Variação de Preços por Período")
    
    produto_var = st.selectbox("Selecione um produto para análise de variação", 
                             df_filtrado['prod_und'].unique(), key='prod_var')
    
    if produto_var:
        df_prod_var = df_filtrado[df_filtrado['prod_und'] == produto_var]
        
        if not df_prod_var.empty:
            # Agrupar por data e calcular média
            ts = df_prod_var.groupby('data')['valor'].mean()
            
            # Verificar se há dados suficientes
            if len(ts) > 1:
                # Calcular variação percentual
                variacao = ts.pct_change() * 100
                
                st.subheader(f"Variação Mensal de Preços para {produto_var}")
                fig, ax = plt.subplots(figsize=(12, 6))
                variacao.plot(ax=ax, marker='o')
                ax.axhline(0, color='red', linestyle='--')
                plt.ylabel('Variação Percentual (%)')
                st.pyplot(fig)
                
                # Maiores variações
                st.subheader("Maiores Variações")
                maiores_var = variacao.sort_values(ascending=False)
                st.dataframe(maiores_var.head(10).to_frame('Variação %').style.format("{:,.2f}%"))
            else:
                st.warning("Dados insuficientes para calcular variação (necessário pelo menos 2 períodos)")
        else:
            st.warning("Nenhum dado disponível para o produto selecionado com os filtros atuais")

# Rodapé
st.sidebar.markdown("---")
st.sidebar.markdown(f"Última atualização: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
