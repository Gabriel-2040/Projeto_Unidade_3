import streamlit as st
from datetime import datetime
from PIL import Image
import os
from utils.data_loader import carregar_dados
from utils.filters import criar_filtros, aplicar_filtros
from utils.visualizations import (
    mostrar_visao_geral,
    mostrar_comparacao_tipos,
    mostrar_instabilidade,
    mostrar_sazonalidade,
    mostrar_variacao_periodo,
    mostrar_plot_mapa_valor,
    
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
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "Visão Geral", 
    "Varejo vs Atacado vs Produtor", 
    "Instabilidade de Preços", 
    "Sazonalidade", 
    "Variação por Período",
    "Mapa valor do produto por estado"
])

with tab1:
    mostrar_visao_geral(df_filtrado)
# Div para observações
    with st.container():
        st.markdown("### Observações")
        st.write("Análise é referente ao faturamento(ganhos) de produtos no mercado brasileiro, separados por\n "
        "estado, ano e tipo de comercialização, região e macrogrupos. Os tipos de comercialização são divididos\n"
        " entre: varejo, atacado e produtor. Nessa aba será verificado:\n\n"
        "   - Estados que mais faturaram\n\n"
        "   - Evolução do faturamento ao longo do tempo(anos)\\nn" 
        "   - 5 produtos que mais faturaram\n\n" )
        # Ou usar um text_area para permitir edição
        observacoes = st.text_area("Adicione suas observações:", key="obs_tab1")
with tab2:
    mostrar_comparacao_tipos(df_filtrado)
    with st.container():
        st.markdown("### Observações")
        st.write("Nessa aba temos 2 gráficos: Um de faturamento do setor(Varejo, Atacado ou Produtor) ao longo dos anos e outro mostrando a distribuição\n" 
        "dos faturamentos por estado.\n\n"
        "No gráfico 1 (Faturamento por Setor p/Ano) conseguimos ver a evolução do faturamento dos setores ao longo dos anos. Podemos usar os filtor de ANOS\n"
        "| ESTADOS | TIPO DE COMERCIALIZAÇÃO(SETOR) | MACROGRUPO. Com suas combinações conseguimos chegar a evolução de faturamento de um estado entre periodos,\n"
        "por tipo de setor, por tipo de produto, conseguindo retirar métricas para decisões\n\n"
        "No gráfico 2 (Distribuição por Estado) conseguimos ver a distribuição de faturamento por estado. E conseguimos ter uma dimensão melhor quanto cada\n"
        "setor infuencia no estado. Podemos usar também os filtros de ANOS | ESTADOS |TIPO DE COMERCIALIZAÇÃO(SETOR) | MACROGRUPO.\n\n"
        "Aqui foi repetido a tabela de os 5 produtos mais vendiddos.")
        # Ou usar um text_area para permitir edição
        observacoes = st.text_area("Adicione suas observações:", key="obs_tab2")

with tab3:
    mostrar_instabilidade(df_filtrado)
    with st.container():
        st.markdown("### Observações")
        st.write("Na tabela de Estado com Maior Variação foi feita uma tabela com a media de preços, desvio padrão e coeficiente de variação. Verificamos que exitem " \
        "muitos valores com diferenças muito altas. A partir disso pelos filtros podemos ir diminuindo a variabilidade\n\n"
        "por macrogrupo, região, estado, espaço de tempo, etc..)\n\n" \
        "**mean ( Media)** : é a média aritmética dos valores por estado. \n\n" \
        "**std (Desvio padrão)** : o desvio padrão, ou seja, o quanto os valores de valor se dispersam em relação à média dentro de cada estado. \n\n" 
        "**cv (Coeficiente de variação)** : Comparar a estabilidade de diferentes grupos: quanto maior o CV, mais instável ou variável é o grupo.")
        # Ou usar um text_area para permitir edição
        observacoes = st.text_area("Adicione suas observações:", key="obs_tab3")

with tab4:
    mostrar_sazonalidade(df_filtrado)
    with st.container():
        st.markdown("### Observações")
        st.write("Aqui temos um gráfico de sazonalidade por mês. Podemos verificar a variação de preco de um produto ao longo do ano.\n\n" \
        "Temos os filtros gerais: MES |ANOS | ESTADOS | TIPO DE COMERCIALIZAÇÃO(SETOR) | MACROGRUPO | REGIAO,  e também tem um \n" \
        "um seletor dopdown onde podemos escolher o produto que queremos analisar ")
        # Ou usar um text_area para permitir edição
        observacoes = st.text_area("Adicione suas observações:", key="obs_tab4")

with tab5:
    mostrar_variacao_periodo(df_filtrado)
    with st.container():
        st.markdown("### Observações")
        st.write("Aqui temos um gráfico de variação em percentual de preços por mês de um produto. Podemos verificar a variação de preco de um produto ao longo do ano.\n\n" \
        "Temos os filtros gerais: MES |ANOS | ESTADOS | TIPO DE COMERCIALIZAÇÃO(SETOR) | MACROGRUPO | REGIAO,  e também tem um \n" \
        "um seletor dopdown onde podemos escolher o produto que queremos analisar ")
        # Ou usar um text_area para permitir edição
        observacoes = st.text_area("Adicione suas observações:", key="obs_tab5")
with tab6:
    mostrar_plot_mapa_valor(df)
    with st.container():
        st.markdown("### Observações")
        st.write("Aqui você pode adicionar suas observações sobre o gráfico acima...")
        # Ou usar um text_area para permitir edição
        observacoes = st.text_area("Adicione suas observações:", key="obs_tab6")

# Rodapé
st.sidebar.markdown("---")
st.sidebar.markdown(f"Última atualização: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")