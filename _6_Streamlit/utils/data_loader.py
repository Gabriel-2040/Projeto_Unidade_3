import pandas as pd
import streamlit as st
from datetime import datetime

def carregar_dados():
    try:
        # Sugiro mover o arquivo para a pasta assets/ ou permitir upload
        df = pd.read_csv('assets/dados_completos.csv')
        
        # Processamento de datas
        df['data'] = pd.to_datetime(df['ano_mes'].astype(str), format='%Y%m')
        df['ano'] = df['data'].dt.year
        df['mes'] = df['data'].dt.month

        if df['data'].isnull().any():
            st.warning("Algumas datas não puderam ser convertidas corretamente")
        
        return df[['estado', 'prod_und', 'tipo_de_comercializacao', 'valor', 'ano', 'mes', 'data', 'macrogrupo']]
    
    except FileNotFoundError:
        st.error("Arquivo de dados não encontrado. Verifique o caminho.")
        return pd.DataFrame()