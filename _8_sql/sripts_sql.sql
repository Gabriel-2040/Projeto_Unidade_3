
create table datawarehouse.dim_produtos(
    id serial primary key,
    prod_und varchar(200),
	macrogrupo_id int
)

select * from datawarehouse.dim_produtos;

create table datawarehouse.dim_nivel_comercializacao(
    id serial PRIMARY KEY,
    tipo_de_comercializacao varchar(100));


create table datawarehouse.dim_estados(
    id serial PRIMARY KEY,
    estado  varchar(2));
    insert into datawarehouse.dim_estados (estado) values
    ('AC'),
    ('AL'),
    ('AP'),
    ('AM'),
    ('BA'),
    ('CE'),
    ('DF'),
    ('ES'),
    ('GO'),
    ('MA'),
    ('MT'),
    ('MS'),
    ('MG'),
    ('PA'),    
    ('PB'),
    ('PR'),    
    ('PE'),
    ('PI'),
    ('RJ'),
    ('RN'),
    ('RS'),
    ('RO'),
    ('RR'),
    ('SC'),
    ('SP'),    
    ('SE'),
    ('TO');
    

create table datawarehouse.dim_macrogrupo(
    id serial PRIMARY KEY,
    macrogrupo varchar(100));

insert into datawarehouse.dim_macrogrupo (macrogrupo) values
('Frutas'),
('Grãos e Cereais'),
('Raízes e Tubérculos'),
('Carnes e Derivados'),
('Lácteos e Ovos'),
('Óleos e Gorduras'),
('Açúcares e Adoçantes'),
('Farinhas e Féculas'),
('Hortaliças e Legumes'),
('Castanhas e Sementes'),
('Bebidas e Extratos'),
('Outros');

create table datawarehouse.microgrupos(
    id serial PRIMARY KEY,
    microgrupo varchar(100));

microgrupo carnes e derivados 
insert into datawarehouse..microgrupos (microgrupo) values
	('Bovinos'),
	('Aves'),
    ('Suínos'),
	('Peixes e Frutos do Mar');

select * from public.microgrupos

create table dim_data(
 id serial primary key,
 mes varchar(100),
 ano integer,
 ano_mes varchar (100));

create table datawarehouse.dim_data(
 id serial primary key,
 mes varchar(100),
 ano integer,
 ano_mes varchar (100));
create table datawarehouse.dim_produtos(
    id serial primary key,
    prod_und varchar(200),
	macrogrupo_id int
)

-- Crie a tabela vazia baseada na estrutura de uma das tabelas
CREATE TABLE datawarehouse.fato_produtos AS
SELECT * FROM public.relatorio_preco_medio_mensal_2014_tratado LIMIT 0;

-- Depois insira os dados
INSERT INTO datawarehouse.fato_produtos
SELECT * FROM public.relatorio_preco_medio_mensal_2014_tratado
UNION ALL
SELECT * FROM public.relatorio_preco_medio_mensal_2015_tratado
union all
SELECT * FROM public.relatorio_preco_medio_mensal_2016_tratado
union all
SELECT * FROM public.relatorio_preco_medio_mensal_2017_tratado
union all
SELECT * FROM public.relatorio_preco_medio_mensal_2018_tratado
union all
SELECT * FROM public.relatorio_preco_medio_mensal_2019_tratado
union all
SELECT * FROM public.relatorio_preco_medio_mensal_2020_tratado
union all
SELECT * FROM public.relatorio_preco_medio_mensal_2021_tratado
union all
SELECT * FROM public.relatorio_preco_medio_mensal_2022_tratado
union all
SELECT * FROM public.relatorio_preco_medio_mensal_2023_tratado

UPDATE datawarehouse.fato_produtos fp
set "Produto/Unidade" = id
from datawarehouse.dim_produtos dp
where dp.prod_und = fp."Produto/Unidade"

UPDATE datawarehouse.fato_produtos fp
set "Nível de Comercialização" = id
from datawarehouse.dim_nivel_comercializacao dnc
where dnc.tipo_de_comercializacao = fp."Nível de Comercialização"

UPDATE datawarehouse.fato_produtos fp
set "U.F." = id
from datawarehouse.dim_estados de
where de.estado = fp."U.F."

UPDATE datawarehouse.fato_produtos fp
set data = id
from datawarehouse.dim_data dt
where dt.ano_mes = fp."U.F."

ALTER TABLE datawarehouse.fato_produtos 
ADD COLUMN id_macrogrupo integer;

ALTER TABLE datawarehouse.fato_produtos 
ALTER COLUMN "id_Produto/Unidade" TYPE integer USING ("id_Produto/Unidade"::integer);

ALTER TABLE datawarehouse.fato_produtos 
ALTER COLUMN "id_Nível de Comercialização" TYPE integer USING ("id_Nível de Comercialização"::integer);

ALTER TABLE datawarehouse.fato_produtos 
ALTER COLUMN "id_U.F." TYPE integer USING ("id_U.F."::integer);

UPDATE datawarehouse.fato_produtos fp
set id_macrogrupo = macrogrupo_id
from datawarehouse.dim_produtos dp
where dp.id = fp."id_Produto/Unidade"

UPDATE datawarehouse.fato_produtos
SET id_data = 
    SUBSTRING(id_data FROM 4 FOR 4) ||  -- Pega o ano (4 caracteres a partir da posição 4)
    SUBSTRING(id_data FROM 1 FOR 2);    -- Pega o mês (2 caracteres a partir da posição 1)

UPDATE datawarehouse.fato_produtos fp
set id_data = id
from datawarehouse.dim_data dt
where dt.ano_mes = fp.id_data

ALTER TABLE datawarehouse.fato_produtos 
ALTER COLUMN "id_data" TYPE integer USING ("id_data"::integer);

SELECT *
FROM datawarehouse.fato_produtos fp
LEFT JOIN datawarehouse.dim_data dd ON dd.id = fp.id_data
LEFT JOIN datawarehouse.dim_estados de ON de.id = fp."id_U.F."
LEFT JOIN datawarehouse.dim_produtos dp ON dp.id = fp."id_Produto/Unidade"
LEFT JOIN datawarehouse.dim_nivel_comercializacao dnc ON dnc.id = fp."id_Nível de Comercialização"
LEFT JOIN datawarehouse.dim_macrogrupo dm ON dm.id = dp.macrogrupo_id
