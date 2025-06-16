import matplotlib.ticker as ticker
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import pandas as pd
import pydeck as pdk
import random
import plotly.express as px


# Dicionário com coordenadas por estado
estados_coords = {
    "AC": [-9.97499, -67.8243], "AL": [-9.5713, -36.782], "AM": [-3.4168, -65.8561],
    "AP": [1.3736, -51.88], "BA": [-12.5797, -41.7007], "CE": [-5.4984, -39.3206],
    "DF": [-15.7998, -47.8645], "ES": [-19.1834, -40.3089], "GO": [-15.827, -49.8362],
    "MA": [-5.0422, -45.3656], "MG": [-18.5122, -44.555], "MS": [-20.7722, -54.7852],
    "MT": [-12.6819, -56.9211], "PA": [-3.4168, -52.2179], "PB": [-7.2399, -36.7819],
    "PE": [-8.8137, -36.9541], "PI": [-7.7183, -42.7289], "PR": [-24.4842, -51.8624],
    "RJ": [-22.9083, -43.1964], "RN": [-5.7945, -36.9541], "RO": [-11.5057, -63.5806],
    "RR": [2.7376, -62.0751], "RS": [-30.0346, -51.2177], "SC": [-27.5954, -48.548],
    "SE": [-10.5741, -37.3857], "SP": [-23.5505, -46.6333], "TO": [-10.1753, -48.2982],
}



def mostrar_visao_geral(df):
    st.header("Visão Geral do Faturamento")
    col1, col2, col3 = st.columns(3)  # Fixed: Added col3 and proper column structure
    with col1:
        _plot_faturamento_estado(df)
    with col2:
        _plot_faturamento_ano(df)
    with col3:
        _plot_top_produtos(df)

def mostrar_comparacao_tipos(df):  # Fixed: Added df parameter
    st.header("Comparação Varejo x Atacado x Produtor")
    col1, col2 = st.columns(2)
    with col1:
        _plot_comparacao_comercializacao(df)  # Fixed: Corrected function name
    with col2:
        _plot_distribuicao_estados(df)

def mostrar_instabilidade(df):  # Fixed: Added df parameter
    st.header("Instabilidade de Preços por Estado")
    col1, col2 = st.columns(2)
    with col1:
        _plot_instabilidade_estados(df)
    with col2:
        _plot_boxplot_estados(df)

def mostrar_mapa_valor(df):
    st.header("Mapa de Valor")
    
    # Adiciona latitude e longitude com base na sigla do estado
    df["latitude"] = df["estado"].map(lambda x: estados_coords.get(x, [None, None])[0])
    df["longitude"] = df["estado"].map(lambda x: estados_coords.get(x, [None, None])[1])

    col1, col2 = st.columns(2)
    with col1:
        mostrar_plot_mapa_valor(df)


def _plot_faturamento_estado(df):
    fat_estado = df.groupby('estado')['valor'].sum().sort_values(ascending=False)
    st.subheader("Faturamento por Estado")
    fig, ax = plt.subplots(figsize=(10, 6))
    fat_estado.plot(kind='bar', ax=ax)
    # Formatar eixo Y como moeda com separador de milhar
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'R$ {x:,.2f}'.replace(",", "X").replace(".", ",").replace("X", ".")))
      # Forçar espaçamento menor entre os ticks
    ax.yaxis.set_major_locator(ticker.MultipleLocator(100000))
    # Subtítulos dos eixos
    ax.set_xlabel("Estados")
    ax.set_ylabel("Faturamento (R$)")
    plt.xticks(rotation=45)
    st.pyplot(fig)

def _plot_faturamento_ano(df):
    st.subheader("Faturamento por Ano")
    fat_ano = df.groupby('ano')['valor'].sum()  # Fixed: Changed df_filtrado to df
    fig, ax = plt.subplots(figsize=(10, 6))
    fat_ano.plot(kind='line', marker='o', ax=ax)
    # Formatar eixo Y como moeda com separador de milhar
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'R$ {x:,.2f}'.replace(",", "X").replace(".", ",").replace("X", ".")))
      # Forçar espaçamento menor entre os ticks
    ax.yaxis.set_major_locator(ticker.MultipleLocator(100000))
    # Subtítulos dos eixos
    ax.set_xlabel("Ano")
    ax.set_ylabel("Faturamento (R$)")
    st.pyplot(fig)

def _plot_top_produtos(df):
    st.subheader("Top 5 Produtos")
    top_prod = df.groupby('prod_und')['valor'].sum().nlargest(5).sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(10, 6))
    top_prod.plot(kind='barh', ax=ax, color='skyblue')
    # Adicionar linhas verticais tracejadas nos pontos de interseção com as barras
    for i, (produto, valor) in enumerate(top_prod.items()):
        ax.axvline(x=valor, color='red', linestyle=':', linewidth=1)
        # (opcional) Adicionar anotação com o valor
        ax.text(valor, i, f'R$ {valor:,.2f}'.replace(",", "X").replace(".", ",").replace("X", "."),
                va='center', ha='left', fontsize=9, color='black')
    # Formatar eixo X (valores)
    ax.xaxis.set_major_formatter(
        ticker.FuncFormatter(lambda x, _: f'R$ {x:,.2f}'.replace(",", "X").replace(".", ",").replace("X", "."))
    )
    ax.xaxis.set_major_locator(ticker.MultipleLocator(100000))
    ax.set_xlabel("Faturamento (R$)")
    ax.set_ylabel("Produtos")    
    plt.tight_layout()
    plt.xticks(rotation=90)
    st.pyplot(fig)

def _plot_comparacao_comercializacao(df):
        
    # 1. Gráfico de faturamento por setor ao longo do tempo
    st.subheader("Faturamento por Setor p/ Ano")
    
    # Agrupar dados por setor e período (mês/ano)
    faturamento_setor = df.groupby(['ano', 'tipo_de_comercializacao'])['valor'].sum().reset_index()
    faturamento_setor['periodo'] = faturamento_setor['ano'].astype(str)
    
    plt.figure(figsize=(12, 6))
    ax = sns.lineplot(
        data=faturamento_setor,
        x='periodo',
        y='valor',
        hue='tipo_de_comercializacao',
        marker='o',
        linewidth=2.5
    )
    
    # Formatar eixo Y
    ax.yaxis.set_major_formatter(
        ticker.FuncFormatter(lambda x, _: f'R$ {x:,.2f}'.replace(",", "X").replace(".", ",").replace("X", "."))
    )
    
    # Adicionar valores nos pontos
    for line in ax.get_lines():
        for x, y in zip(line.get_xdata(), line.get_ydata()):
            ax.text(x, y, f'R$ {y:,.0f}'.replace(",", "X").replace(".", ",").replace("X", "."),
                    color='black', fontsize=8, ha='center', va='bottom')
    
    plt.xlabel("Período (Ano)")
    plt.ylabel("Faturamento Total")
    plt.xticks(rotation=90)
    plt.legend(title='Setor', loc='upper left')
    plt.tight_layout()
    st.pyplot(plt.gcf())
    
    # 2. Tabela com os 5 produtos mais vendidos
    st.subheader("Top 5 Produtos Mais Vendidos")
    
    # Calcular top produtos
    top_produtos = df.groupby('prod_und')['valor'].sum().nlargest(5).reset_index()
    top_produtos = top_produtos.rename(columns={
        'prod_und': 'Produto',
        'valor': 'Faturamento Total'
    })
    
    # Formatar valores monetários
    top_produtos['Faturamento Total'] = top_produtos['Faturamento Total'].apply(
        lambda x: f'R$ {x:,.2f}'.replace(",", "X").replace(".", ",").replace("X", ".")
    )
    
    # Adicionar posição (ranking)
    top_produtos.insert(0, 'Posição', range(1, 6))
    
    # Exibir tabela formatada
    st.table(top_produtos)

def _plot_distribuicao_estados(df):
    st.subheader("Distribuição por Estado")

    # Totais nacionais
    totais_nacionais = df.groupby('tipo_de_comercializacao')['valor'].sum()

    # Pivot com ordenação automática das colunas
    pivot = pd.pivot_table(df, values='valor', index='estado',
                           columns='tipo_de_comercializacao', aggfunc='sum').fillna(0)
    pivot = pivot[totais_nacionais.sort_values().index]

    # Ordena estados pelo total
    pivot['TOTAL'] = pivot.sum(axis=1)
    pivot = pivot.sort_values(by='TOTAL').drop(columns='TOTAL')
    pivot = pivot.iloc[::-1]  # Inverte ordem para maior no topo

    # PALETA PERSONALIZADA CONFORME SUA REQUISIÇÃO
    cores_personalizadas = {
        'atacado': '#1f77b4',   # Azul
        'varejo': '#2ca02c',     # Verde
        'produtor': '#ff7f0e',    # Laranja
    }
    
    # # Garante que todas as colunas tenham cores (usa cinza para tipos não especificados)
    # cores = [cores_personalizadas.get(col, '#999999') for col in pivot.columns]

    # Plot
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.yaxis.set_major_formatter(
        ticker.FuncFormatter(lambda x, _: f'R$ {x:,.2f}'.replace(",", "X").replace(".", ",").replace("X", "."))
    )
    
    # Gráfico com cores personalizadas
    pivot.plot(kind='bar', stacked=True, ax=ax, color=cores)

    plt.xticks(rotation=45)
    plt.legend(title='Tipo de Comercialização', loc='upper left', bbox_to_anchor=(1, 1))
    plt.tight_layout()
    st.pyplot(fig)


def _plot_instabilidade_estados(df):
    # Calcular coeficiente de variação
    cv_estado = df.groupby('estado')['valor'].agg(['mean', 'std'])
    cv_estado['cv'] = (cv_estado['std'] / cv_estado['mean']) * 100
    cv_estado = cv_estado.sort_values('cv', ascending=False)
    st.subheader("Estados com Maior Instabilidade")
    st.dataframe(cv_estado.style.format("{:,.2f}"))

def _plot_boxplot_estados(df):
    st.subheader("Distribuição de Preços por Estado")
    fig, ax = plt.subplots(figsize=(14, 8))
        # Formatar eixo Y como moeda com separador de milhar
    ax.yaxis.set_major_formatter(
        ticker.FuncFormatter(lambda x, _: f'R$ {x:,.2f}'.replace(",", "X").replace(".", ",").replace("X", "."))
    )
    sns.boxplot(data=df, x='estado', y='valor', ax=ax)
    ax.set_xlabel("ESTADOS")
    ax.set_ylabel("Faturamento (R$)")
    plt.xticks(rotation=45)
    st.pyplot(fig)

def mostrar_sazonalidade(df):
    st.header("Análise de Sazonalidade")
        
    produto_selecionado = st.selectbox("Selecione um produto", df['prod_und'].unique())
        
    # Dados do produto selecionado
    df_produto = df[df['prod_und'] == produto_selecionado]
    
    if not df_produto.empty:
        # Sazonalidade por mês
        sazonal = df_produto.groupby(['ano', 'mes'])['valor'].sum().unstack(level=0)
        
        st.subheader(f"Sazonalidade para {produto_selecionado}")
        fig, ax = plt.subplots(figsize=(10, 3))
        ax.yaxis.set_major_formatter(
        ticker.FuncFormatter(lambda x, _: f'R$ {x:,.2f}'.replace(",", "X").replace(".", ",").replace("X", "."))
    )
        # Legenda fora do gráfico, alinhada à direita com espaçamento
        ax.legend(title='Ano', bbox_to_anchor=(1.15, 1), loc='upper left', fontsize=8, title_fontsize=9)

        sazonal.plot(ax=ax)
        plt.legend(title='Ano', bbox_to_anchor=(1.05, 1), loc='upper left')
        # Tamanhos de fonte menores
        ax.tick_params(axis='both', labelsize=8)
        plt.tight_layout(pad=0.5)
        st.pyplot(fig)
        
        # Meses sem venda
        meses_sem_venda = sazonal[sazonal.isnull().any(axis=1)]
        if not meses_sem_venda.empty:
            st.warning(f"Meses sem vendas para {produto_selecionado}: {list(meses_sem_venda.index)}")
    else:
        st.warning("Nenhum dado disponível para o produto selecionado com os filtros atuais") 


def mostrar_variacao_periodo(df):
    st.header("Variação de Preços por Período")
    
    produto_var = st.selectbox("Selecione um produto para análise de variação", 
                             df['prod_und'].unique(), key='prod_var')
    
    if produto_var:
        df_prod_var = df[df['prod_und'] == produto_var]
        
        if not df_prod_var.empty:
            # Agrupar por data e calcular média
            ts = df_prod_var.groupby('data')['valor'].mean()
            
            # Verificar se há dados suficientes
            if len(ts) > 1:
                # Calcular variação percentual
                variacao = ts.pct_change() * 100
                
                st.subheader(f"Variação Mensal de Preços para {produto_var}")
                fig, ax = plt.subplots(figsize=(12, 4))
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

def mostrar_plot_mapa_valor(df):
    st.subheader("Mapa de Valor por Estado")

    # Adiciona latitude/longitude se necessário
    if 'latitude' not in df.columns or 'longitude' not in df.columns:
        df["latitude"] = df["estado"].map(lambda x: estados_coords.get(x, [None, None])[0])
        df["longitude"] = df["estado"].map(lambda x: estados_coords.get(x, [None, None])[1])

    df = df.dropna(subset=["latitude", "longitude"])

    # Agrupamento
    df_mapa = df.groupby(['estado', 'prod_und', 'latitude', 'longitude'], as_index=False)['valor'].sum()

    # Normalizar valores para melhor visualização
    max_valor = df_mapa['valor'].max()
    df_mapa['raio_normalizado'] = 50000 + (df_mapa['valor'] / max_valor) * 500000

    # Gerar cores mais claras e vivas
    produtos_unicos = df_mapa["prod_und"].unique()
    cores_aleatorias = {
        produto: [
            random.randint(150, 255),  # R - mais claro
            random.randint(150, 255),  # G - mais claro
            random.randint(50, 200),   # B - variado
            200                        # Alpha - mais opaco
        ]
        for produto in produtos_unicos
    }

    df_mapa["color"] = df_mapa["prod_und"].apply(lambda x: cores_aleatorias.get(x, [200, 200, 200, 200]))

    # Tooltip para mostrar informações
    tooltip = {
        "html": "<b>Estado:</b> {estado}<br>"
                "<b>Produto:</b> {prod_und}<br>"
                "<b>Valor:</b> R$ {valor:,.2f}",
        "style": {
            "backgroundColor": "steelblue",
            "color": "white"
        }
    }

    layer = pdk.Layer(
        "ScatterplotLayer",
        data=df_mapa,
        get_position='[longitude, latitude]',
        get_radius="raio_normalizado",  # Usar raio normalizado
        get_fill_color="color",
        pickable=True,
        auto_highlight=True,
    )

    view_state = pdk.ViewState(
        latitude=-14.2350,
        longitude=-51.9253,
        zoom=3.2,  # Zoom um pouco mais próximo
        pitch=0,   # Inclinação para melhor perspectiva
        bearing=0
    )

    # Usar mapa claro
    r = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip=tooltip,
        map_style='light'  # Estilo de mapa claro
    )

    st.pydeck_chart(r)