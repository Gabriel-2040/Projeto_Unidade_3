import matplotlib.ticker as ticker
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import pandas as pd

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
        _plot_distribuicao_tipos(df)

def mostrar_instabilidade(df):  # Fixed: Added df parameter
    st.header("Instabilidade de Preços por Estado")
    col1, col2 = st.columns(2)
    with col1:
        _plot_instabilidade_estados(df)
    with col2:
        _plot_boxplot_estados(df)

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
    st.subheader("Faturamento por Tipo")
    plt.style.use('default')
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.boxplot(data=df, x='tipo_de_comercializacao', y='valor', ax=ax)

    # Formatar eixo Y como moeda com separador de milhar
    ax.yaxis.set_major_formatter(
        ticker.FuncFormatter(lambda x, _: f'R$ {x:,.2f}'.replace(",", "X").replace(".", ",").replace("X", "."))
    )

    # Ajustar os ticks com base no valor máximo
    max_valor = df['valor'].max()
    ax.yaxis.set_major_locator(ticker.MultipleLocator(max_valor / 5))

    # Cor dos labels para garantir visibilidade
    for label in ax.get_yticklabels():
        label.set_color('black')

    # Subtítulos dos eixos
    ax.set_xlabel("Produtor | Atacado | Varejo")
    ax.set_ylabel("Faturamento (R$)")
    plt.xticks(rotation=45)
    st.pyplot(fig)

def _plot_distribuicao_tipos(df):
    st.subheader("Distribuição por Estado")
    pivot = pd.pivot_table(df, values='valor', index='estado', 
                          columns='tipo_de_comercializacao', aggfunc='sum')
    fig, ax = plt.subplots(figsize=(12, 8))
    pivot.plot(kind='bar', stacked=True, ax=ax)
    plt.xticks(rotation=45)
    plt.legend(title='Tipo Comercialização')
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
    sns.boxplot(data=df, x='estado', y='valor', ax=ax)
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
        fig, ax = plt.subplots(figsize=(12, 8))
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