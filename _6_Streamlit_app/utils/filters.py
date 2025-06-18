import pandas as pd
import streamlit as st
from datetime import datetime


def criar_filtros(df):
    st.sidebar.header('Filtros')
    
    return {
        'meses': st.sidebar.multiselect(
            'Meses', 
            options=sorted(df['mes'].unique()), 
            default=sorted(df['mes'].unique())
        ),
        'anos': st.sidebar.multiselect(
            'Anos', 
            options=sorted(df['ano'].unique()), 
            default=sorted(df['ano'].unique())
        ),
        'estados': st.sidebar.multiselect(
            'Estados', 
            options=sorted(df['estado'].unique()), 
            default=sorted(df['estado'].unique())
        ),
        'tipos_comerc': st.sidebar.multiselect(
            'Tipo Comercialização', 
            options=sorted(df['tipo_de_comercializacao'].unique()), 
            default=sorted(df['tipo_de_comercializacao'].unique())
        ),
        'macrogrupos': st.sidebar.multiselect(
            'Macrogrupos', 
            options=sorted(df['macrogrupo'].unique()), 
            default=sorted(df['macrogrupo'].unique())
        ),
        'regioes': st.sidebar.multiselect(
            'Região', 
            options=sorted(df['nome_regiao'].unique()), 
            default=sorted(df['nome_regiao'].unique())
        )
    }

def aplicar_filtros(df, filtros):
    return df[
        (df['mes'].isin(filtros['meses'])) &
        (df['ano'].isin(filtros['anos'])) & 
        (df['estado'].isin(filtros['estados'])) & 
        (df['tipo_de_comercializacao'].isin(filtros['tipos_comerc'])) &
        (df['macrogrupo'].isin(filtros['macrogrupos'])) &
        (df['nome_regiao'].isin(filtros['regioes']))  # Corrigido para nome_regiao
    ]
    