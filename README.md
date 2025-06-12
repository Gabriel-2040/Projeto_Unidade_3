# Projeto de Analise de Dados - Disciplina de Python - Digital College
### Professora Nayara Valevskii
## Base de dados : 
#### Entendimento do Negócio
Essa base representa os preços mensais de produtos agrícolas e alimentícios no Brasil, divulgados por órgãos oficiais, em diferentes níveis de comercialização (produtor, atacado, varejo) e por Unidade Federativa (U.F.).
Você atuará como um analista de dados para uma secretaria de políticas públicas, com a missão de monitorar inflação
setorial, flutuações regionais e apoiar decisões estratégicas sobre produção, subsídios ou políticas de abastecimento.
## Etapa de Analise exporatoria.
- Primeiros codigos, testes, verificações, tentativas. os codigos aqui não são usados nas outras etapas. São verificação dos tipos de dados, primeiras colunas, vericação de nulos, vazios, cabeçalhos(head) e rodapés(tail). A partir daqui foram tomadas as primeiras decisões.
<p align="center">
  <img src="https://github.com/Gabriel-2040/Projeto_Unidade_3/blob/main/_10_imagens/bases.JPG" alt="bases" />
</p>
<p align="center">
  <img src="https://github.com/Gabriel-2040/Projeto_Unidade_3/blob/main/_10_imagens/dataset%20incial_head.JPG" alt="dataset incial_head" />
</p>
<p align="center">
  <img src="https://github.com/Gabriel-2040/Projeto_Unidade_3/blob/main/_10_imagens/dataset%20incial_tail.JPG" alt="dataset incial_tail" />
</p>
## Etapa de ETL
Etapa onde se realizam os processos de tratamento dos dados e inserção no banco de dados.
<p align="center">
  <img src="https://github.com/Gabriel-2040/Projeto_Unidade_3/blob/main/_10_imagens/dados%20etl.JPG" alt="dados etl" />
</p>
#### Arquivo: ./datasets_tratados/tratamento_dataset.ipynb
- 1 tratamento do dataset original. preenchimento de nulos com 0.
- Remoção do rodapé com textos desnecessários. 
- Retirada de linhas vazias.
<p align="center">
  <img src="https://github.com/Gabriel-2040/Projeto_Unidade_3/blob/main/_10_imagens/dataset_n%C3%A3o%20rotacionado.JPG" alt="dataset_não rotacionado" />
</p>

#### Arquivo : .datasets_rotacionados/ rotacionar_csv.ipynb
- Aqui o codigo é feito pra rotacionar a tabela deixando com as colunas (Produto/Unidade,Nível de Comercialização,U.F.,data,valor)
para inserir no postgres foi necessário retirar a virgula e o ponto da cassa do milhar e deixar nesse formato 10000.00
<p align="center">
  <img src="https://github.com/Gabriel-2040/Projeto_Unidade_3/blob/main/_10_imagens/dataset%20rotacionado.JPG" alt="dataset rotacionado" />
</p>
#### Arquivo: ./merge_csv/merge_colunas.ipynb 
- Arquivo feito para criar as dimensões. crias os csv para fazer os produtos e os tipos de comercio.
#### Nesse tempo foi criada uma pasta funções pois alguns codigos estavam se replicando muito. As funções criadas são:
- atualizar_macrogrupo.py
- conectar_banco.py (concetar com banco de dados)
- fechar_conexao (fechar conexão com banco)
<p align="center">
  <img src="https://github.com/Gabriel-2040/Projeto_Unidade_3/blob/main/_10_imagens/datawarehouse.JPG" alt="datawarehouse" />
</p>
#### No arquivo ./_4_Etapa_ETL/ insert_public, foram inseridos os dados nas dimensões.
- datawarehouse.dim_produtos - dados de merge_colunas.ipynb - quem gerou o merge_colunas_produtos.Todos os produtos.
- datawarehouse.dim_nivel_comercializacao - tipos de Comercialização (produtors, varejo, atacado)
- datawarehouse.dim_data - dimensão tempo 
- datawarehosue.dim_regioes - (não foi adicionado nessa etapa, só depois se viu a necessidade dessa dimensão para análise das regiões, norte, nordeste, etc).
- datawarehouse.dim_macrogrupo
Foi notado que seria interessante verificar os macrogrupos, frutas, cereais, etc..Assim foi criado uma
nova coluna chamada macrogrupo. Adicionado a fk na tabela dim_produtos e feita a dimensão macrogrupos.
- datawarehouse.fato_produtos - feita por sql (queries no arquivo ./_8_sql/scricpts_sql.sql)
##### Aqui com as dimensões e a tabela_fato feita fiz o download do csv pois verifiquei que poderia tratar os dados diretamente com python, sem precisar ficar acessando do banco (que no final acaba sendo uma boa pratica). com o codigo ./
<p align="center">
  <img src="https://github.com/Gabriel-2040/Projeto_Unidade_3/blob/main/_10_imagens/modelo%20relacional%20datawarehouse.JPG" alt="modelo relacional datawarehous" />
</p>
_5_Dataframes_tratados/conexao.ipynb
A concepção das dimensões, ajudou a guardar os dados tratados e poder fazer o download do arquvio completo csv. A partir desse momento iniciou uma outraa etapara chamada.
## _5_Dataframes_Tratados
Verificou-se até esse momento que se tratava de um conjunto de dados que releava sobre o faturamento bruto de um estado no que tange aos produtos vendidos de qualquer origem legal, diferenciados
somente pelo tipo de produto, a origem do faturamento(estado) e quem foi que o comercializou se foi um comércio -Varejista, Atacadista ou foi direto do produtor.
Assim se iniciou a responder algumas questões: 
- Diferença entre o Varejo, Atacado, e produtor.
- Instabilidade de preços dos produtos
- Quantidade de produtos vendidos por ano
- Verificar a sazonabilidade dos produtos
Verificando essas respostas usando a biblioteca pandas para gerar alguns graficos, nos foi dada a oportunidade de conhecer uma ferramente de DataViz chamada Streamlit. que vem a ser o passo seguinte.
<p align="center">
  <img src="https://github.com/Gabriel-2040/Projeto_Unidade_3/blob/main/_10_imagens/dataframe%20tratado.JPG" alt="dataframe tratado" />
</p>
## _6_Streamlit
O Streamlit é uma biblioteca que possibilita que se monte paineis interativos com funções pyhton. A diferença é que ele não roda arquivos .ipynb, mas .py. Dessa forma foi preciso pegar as respostas respondidas no item anterior (_5_Dataframes_Tratados) e ajustar no formato do Streamlit.
Nele você pode adicionar filtros, nas paginas e usar todo potencial do pandas, seaborn com os graficos.
Podemos adicionar botões etc. Como projeto ainda não esta finalizado, preteno ajustar com algumas funções que tem na bilioteca para demonstrar melhor a ferramenta.
Vou adicionar (daqui a pouco) um link com um video curto do trabalho.

<p align="center">
  <img src="https://github.com/Gabriel-2040/Projeto_Unidade_3/blob/main/_10_imagens/dataframe%20tratado.JPG" alt="record_2025-06-11_23-19-14" />
</p>


