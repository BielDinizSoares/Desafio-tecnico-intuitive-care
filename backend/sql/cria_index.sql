CREATE INDEX idx_operadora_cnpj
ON operadora (cnpj);

CREATE INDEX idx_despesa_ano_trimestre
ON despesa_consolidada (ano, trimestre);

CREATE INDEX idx_despesa_operadora
ON despesa_consolidada (id_operadora);
