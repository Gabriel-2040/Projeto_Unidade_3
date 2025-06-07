import streamlit as st
from datetime import datetime
from utils.data_loader import carregar_dados
from utils.filters import criar_filtros, aplicar_filtros
from utils.visualizations import (
    mostrar_visao_geral,
    mostrar_comparacao_tipos,
    mostrar_instabilidade,
    mostrar_sazonalidade,
    mostrar_variacao_periodo
)

# Configuração inicial
st.set_page_config(layout="wide", page_title="Análise de Comercialização")

# Carregar dados
df = carregar_dados()
if df.empty:
    st.error("Erro: Nenhum dado foi carregado. Verifique a fonte de dados.")
    st.stop()

# Sidebar - Filtros
filtros = criar_filtros(df)  # Corrigido o nome da função aqui
df_filtrado = aplicar_filtros(df, filtros)

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
    mostrar_visao_geral(df_filtrado)
# Div para observações
    with st.container():
        st.markdown("### Observações")
        st.write("O banco de dados é referente ao faturamento(ganhos) de produtos no mercado brasileiro, separados por\n "
        "estado, ano e tipo de comercialização, sendo varejo, atacado e produtor. Aqui vamos verificar:\n"
        "   - Estados que mais faturaram\n"
        "   - Evolução do faturamento ao longo do tempo\n" 
        "   - Tipos de  produtos que mais faturaram\n" )
        # Ou usar um text_area para permitir edição
        observacoes = st.text_area("Adicione suas observações:", key="obs_tab1")
with tab2:
    mostrar_comparacao_tipos(df_filtrado)
    with st.container():
        st.markdown("### Observações")
        st.write("Aqui você pode adicionar suas observações sobre o gráfico acima...")
        # Ou usar um text_area para permitir edição
        observacoes = st.text_area("Adicione suas observações:", key="obs_tab2")

with tab3:
    mostrar_instabilidade(df_filtrado)
    with st.container():
        st.markdown("### Observações")
        st.write("Aqui você pode adicionar suas observações sobre o gráfico acima...")
        # Ou usar um text_area para permitir edição
        observacoes = st.text_area("Adicione suas observações:", key="obs_tab3")

with tab4:
    mostrar_sazonalidade(df_filtrado)
    with st.container():
        st.markdown("### Observações")
        st.write("Aqui você pode adicionar suas observações sobre o gráfico acima...")
        # Ou usar um text_area para permitir edição
        observacoes = st.text_area("Adicione suas observações:", key="obs_tab4")

with tab5:
    mostrar_variacao_periodo(df_filtrado)
    with st.container():
        st.markdown("### Observações")
        st.write("Aqui você pode adicionar suas observações sobre o gráfico acima...")
        # Ou usar um text_area para permitir edição
        observacoes = st.text_area("Adicione suas observações:", key="obs_tab5")

# Rodapé
st.sidebar.markdown("---")
st.sidebar.markdown(f"Última atualização: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")