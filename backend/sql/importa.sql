\copy operadora (registro_operadora, cnpj, razao_social, nome_fantasia, modalidade, logradouro, numero, complemento, bairro, cidade, uf, cep, ddd, telefone, fax, endereco_eletronico, representante, cargo_representante, regiao_de_comercializacao, data_registro_ans) FROM 'data/Relatorio_cadop.csv' DELIMITER ';' CSV HEADER ENCODING 'UTF8';

\copy despesa_trimestral (cnpj, razao_social, trimestre, ano, valor_despesas) FROM 'data/consolidados_despesas.csv' DELIMITER ';' CSV HEADER ENCODING 'UTF8';

\copy despesa_agregada (razao_social, uf, valor_despesas) FROM 'data/despesas_agregadas.csv' DELIMITER ';' CSV HEADER ENCODING 'UTF8';
