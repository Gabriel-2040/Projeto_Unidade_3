import pandas as pd
import streamlit as st
from datetime import datetime

def criar_filtros(df):
    st.sidebar.header('Filtros')
    
    return {
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
        'Macrogrupos': st.sidebar.multiselect(
        'Macrogrupos', 
        options=sorted(df['macrogrupo'].unique()), 
        default=sorted(df['macrogrupo'].unique())
        )
    }
    

def aplicar_filtros(df, filtros):
    return df[
        (df['ano'].isin(filtros['anos'])) & 
        (df['estado'].isin(filtros['estados'])) & 
        (df['tipo_de_comercializacao'].isin(filtros['tipos_comerc'])) &
        (df['macrogrupo'].isin(filtros['Macrogrupos']))
    ]