import pandas as pd
import streamlit as st
from datetime import datetime


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
