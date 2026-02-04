# IntuitiveCare - Desafio Técnico

## Teste 1 - Web Scraping e Processamento de Dados

No notebook de data anaylisis, optei por processar os arquivos em chunks de 100 mil, por meio da função api_requests, usando protocolo https. A função baixa e descompacta, criando um diretório data. Após isso, analisei as colunas dos DF dos trimestres de 2025, e notei duas colunas importantes: DESCRICAO e CD_CONTA_CONTABIL. A primeira abordagem foi tentar identificar qual CD_CONTA_CONTABIL seria relacionado a eventos / sinistros, porém acabei notando que não está padronizado, e pela descrição vários outros dados estavam passando. Optei então por identificar a string de descrição, normalizando tudo da coluna para upper e identifiquei eventos e sinistros utilizando regex . Assim, foi feita a consolidação dos dados em um único csv, eventos_sinistros_2025.

## Teste 2 - Tratamento de Dados

### Tratamentos aplicados:
- **Valores NULL em campos obrigatórios**: Removidos registros com CNPJ, Razão Social ou Registro ANS vazios
- **Strings em campos numéricos**: Uso de `pd.to_numeric(errors='coerce')` para converter, valores inválidos viram NaN
- **Datas inconsistentes**: Uso de `pd.to_datetime(errors='coerce')` para padronizar formato YYYY-MM-DD
- **Validação de CNPJ**: Biblioteca `validate-docbr` para validar CNPJs
- **Duplicatas**: Removidas por CNPJ + Trimestre

## Teste 3 - Banco de Dados

Tabelas criadas:
- `operadora` - Dados do Relatorio_cadop.csv
- `despesa_trimestral` - Dados consolidados por trimestre
- `despesa_agregada` - Dados agregados por operadora/UF

**Decisão de não normalizar**: Com apenas ~1500 registros de despesas e ~1100 operadoras, a normalização adicionaria complexidade desnecessária. O volume não justifica JOINs adicionais.

## Teste 4 - API REST

### Rotas implementadas:

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/operadoras` | Lista operadoras com paginação |
| GET | `/operadoras/busca?q=termo` | Busca por razão social ou CNPJ |
| GET | `/operadoras/{registro}` | Detalhe de uma operadora |
| GET | `/despesas/trimestral` | Lista despesas trimestrais |
| GET | `/despesas/agregadas` | Lista despesas agregadas |
| GET | `/despesas/top10` | Top 10 maiores despesas |

### Paginação por Offset - Justificativa

Optei por **paginação por offset** (`LIMIT/OFFSET`) ao invés de cursor-based pelos seguintes motivos:

1. **Volume pequeno de dados**: Com ~1100 operadoras e ~1500 despesas, o overhead do offset é desprezível. O problema de performance do offset (scan de N registros) só se manifesta com milhões de registros.

2. **Simplicidade de implementação**: Offset permite navegação direta para qualquer página (`?offset=50&limite=10` = página 6), enquanto cursor exige navegação sequencial.

3. **Compatibilidade com UI**: A maioria das bibliotecas de tabela/grid (DataTables, AG Grid, etc) espera paginação por offset com `total` de registros.

4. **Ordenação flexível**: Offset permite ordenar por qualquer coluna sem precisar de índice específico. Cursor-based exige que a coluna de cursor seja única e indexada.

**Trade-off aceito**: Em datasets maiores (>100k registros), cursor-based seria preferível para evitar o scan. Para este caso, offset é a escolha pragmática.

### Como executar a API:

```bash
cd backend
pip install fastapi uvicorn psycopg2-binary
uvicorn api.main:app --reload
```

Acesse: http://localhost:8000/docs para documentação Swagger.