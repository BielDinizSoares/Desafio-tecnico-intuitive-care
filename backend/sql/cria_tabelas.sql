CREATE TABLE operadora (
    id_operadora SERIAL PRIMARY KEY,

    registro_operadora VARCHAR(20) UNIQUE NOT NULL,
    cnpj VARCHAR(18) NOT NULL,

    razao_social TEXT NOT NULL,
    nome_fantasia TEXT,

    modalidade VARCHAR(50),

    logradouro TEXT,
    numero TEXT,
    complemento TEXT,
    bairro TEXT,
    cidade TEXT,
    uf CHAR(2),
    cep VARCHAR(10),

    ddd VARCHAR(3),
    telefone VARCHAR(20),
    fax VARCHAR(20),
    endereco_eletronico TEXT,

    representante TEXT,
    cargo_representante TEXT,

    regiao_de_comercializacao TEXT,

    data_registro_ans DATE
);

CREATE TABLE despesa_trimestral (
    id_despesa SERIAL PRIMARY KEY,
    cnpj VARCHAR(18) NOT NULL,
    razao_social TEXT NOT NULL,
    trimestre VARCHAR(2) NOT NULL,
    ano VARCHAR(4) NOT NULL,
    valor_despesas BIGINT NOT NULL
);

CREATE TABLE despesa_agregada (
    id_agregado SERIAL PRIMARY KEY,
    razao_social TEXT NOT NULL,
    uf CHAR(2),
    valor_despesas BIGINT NOT NULL
);
