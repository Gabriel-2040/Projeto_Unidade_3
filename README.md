# Projeto de Analise de Dados - Disciplina de Python - Digital College
### Professora Nayara Valevskii
## Base de dados : 
#### Entendimento do Negócio
Essa base representa os preços mensais de produtos agrícolas e alimentícios no Brasil, divulgados por órgãos oficiais,
em diferentes níveis de comercialização (produtor, atacado, varejo) e por Unidade Federativa (U.F.).
Você atuará como um analista de dados para uma secretaria de políticas públicas, com a missão de monitorar inflação
setorial, flutuações regionais e apoiar decisões estratégicas sobre produção, subsídios ou políticas de abastecimento.
## Etapa de Analise exporatoria.
Primeiros codigos, testes, verificações, tentativas. os codigos aqui não são usados nas outras etapas. São verificação dos tipos de dados, primeiras colunas,
vericação de nulos, vazios, cabeçalhos(head) e rodapés(tail). A partir daqui são tomadas as primeiras decisões.
## Etapa de ETL
Etapa onde se realizam os processos de tratamento dos dados e inserção no banco de dados.
### Arquivo: ./datasets_tratados/tratamento_dataset.ipynb
    - 1 tratamento do dataset original. preenchimento de nulos com 0.
    - Remoção do rodapé com textos desnecessários. 
    - Retirada de linhas vazias.
#### Arquivo : .datasets_rotacionados/ rotacionar_csv.ipynb
    - Aqui o codigo é feito pra rotacionar a tabela deixando com as colunas (Produto/Unidade,Nível de Comercialização,U.F.,data,valor)
    para inserir no postgres foi necessário retirar a virgula e o ponto da cassa do milhar e deixar nesse formato 10000.00
#### Arquivo: ./merge_csv/merge_colunas.ipynb 
    - Arquivo feito para criar as dimensões. crias os csv para fazer os produtos e os tipos de comercio.
#### Nesse tempo foi criada uma pasta funções pois alguns codigos estavam se replicando muito. As funções criadas são:
    - atualizar_macrogrupo.py
    - conectar_banco.py (concetar com banco de dados)
    - fechar_conexao (fechar conexão com banco)
#### No arquivo ./_4_Etapa_ETL/ insert_public, foram inseridos os dados nas dimensões.
    - datawarehouse.dim_produtos - dados de merge_colunas.ipynb - quem gerou o merge_colunas_produtos.Todos os produtos.
    - datawarehouse.dim_nivel_comercializacao - tipos de Comercialização (produtors, varejo, atacado)
    - datawarehouse.dim_data - dimensão tempo 
    - datawarehosue.dim_regioes - (não foi adicionado nessa etapa, só depois se viu a necessidade dessa dimensão para análise das regiões, norte, nordeste, etc).
    - datawarehouse.dim_macrogrupo
        Foi notado que seria interessante verificar os macrogrupos, frutas, cereais, etc..Assim foi criado uma
        nova coluna chamada macrogrupo. Adicionado a fk na tabela dim_produtos e feita a dimensão macrogrupos.
    - datawarehouse.fato_produtos - feita por sql (queries no arquivo ./_8_sql/scricpts_sql.sql)
Aqui com as dimensões e a tabela_fato feita fiz o download do csv pois verifiquei que pdeoria tratar os dados auqi com python  precisar ficar pegando do banco( boa pratica). com o codigo ./_5_Dataframes_tratados/conexao.ipynb
    A concepção das dimensões, ajudou a guardar os dados tratados e poder fazer o download do arquvio completo csv. A parti disso 




