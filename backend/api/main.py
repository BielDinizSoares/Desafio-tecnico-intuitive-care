from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import Optional

app = FastAPI(
    title="API Operadoras ANS",
    description="API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


DB_CONFIG = {
    "host": "localhost",
    "database": "teste_intuitive_care",
    "user": "gabriel",
    "password": "gabriel"
}

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG, cursor_factory=RealDictCursor)



@app.get("/operadoras")
def listar_operadoras(
    limite: int = Query(default=10, ge=1, le=100, description="Quantidade de registros"),
    offset: int = Query(default=0, ge=0, description="Pular N registros"),
    uf: Optional[str] = Query(default=None, description="Filtrar por UF")
):
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    if uf:
        cur.execute(
            "SELECT * FROM operadora WHERE uf = %s ORDER BY razao_social LIMIT %s OFFSET %s",
            (uf.upper(), limite, offset)
        )
    else:
        cur.execute(
            "SELECT * FROM operadora ORDER BY razao_social LIMIT %s OFFSET %s",
            (limite, offset)
        )
    
    operadoras = cur.fetchall()
    
 
    cur.execute("SELECT COUNT(*) as total FROM operadora")
    total = cur.fetchone()["total"]
    
    cur.close()
    conn.close()
    
    return {
        "data": operadoras,
        "total": total,
        "limite": limite,
        "offset": offset
    }


@app.get("/operadoras/busca")
def buscar_operadoras(
    q: str = Query(..., min_length=2, description="Termo de busca (razão social ou CNPJ)"),
    limite: int = Query(default=10, ge=1, le=100)
):
   
    conn = get_db_connection()
    cur = conn.cursor()
    
    termo = f"%{q}%"
    cur.execute(
        """
        SELECT * FROM operadora 
        WHERE razao_social ILIKE %s OR cnpj LIKE %s
        ORDER BY razao_social
        LIMIT %s
        """,
        (termo, termo, limite)
    )
    
    operadoras = cur.fetchall()
    cur.close()
    conn.close()
    
    return {"data": operadoras, "total": len(operadoras)}


@app.get("/operadoras/{registro}")
def obter_operadora(registro: str):
    """
    Retorna uma operadora pelo registro ANS.
    """
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("SELECT * FROM operadora WHERE registro_operadora = %s", (registro,))
    operadora = cur.fetchone()
    
    cur.close()
    conn.close()
    
    if not operadora:
        raise HTTPException(status_code=404, detail="Operadora não encontrada")
    
    return operadora




@app.get("/despesas/trimestral")
def listar_despesas_trimestrais(
    limite: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    trimestre: Optional[str] = Query(default=None, description="Filtrar por trimestre (1T, 2T, 3T)"),
    ano: Optional[str] = Query(default=None, description="Filtrar por ano")
):
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    query = "SELECT * FROM despesa_trimestral WHERE 1=1"
    params = []
    
    if trimestre:
        query += " AND trimestre = %s"
        params.append(trimestre)
    if ano:
        query += " AND ano = %s"
        params.append(ano)
    
    query += " ORDER BY valor_despesas DESC LIMIT %s OFFSET %s"
    params.extend([limite, offset])
    
    cur.execute(query, params)
    despesas = cur.fetchall()
    
    cur.close()
    conn.close()
    
    return {"data": despesas, "limite": limite, "offset": offset}


@app.get("/despesas/agregadas")
def listar_despesas_agregadas(
    limite: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    uf: Optional[str] = Query(default=None, description="Filtrar por UF")
):
    """
    Lista despesas agregadas por operadora/UF.
    """
    conn = get_db_connection()
    cur = conn.cursor()
    
    if uf:
        cur.execute(
            "SELECT * FROM despesa_agregada WHERE uf = %s ORDER BY valor_despesas DESC LIMIT %s OFFSET %s",
            (uf.upper(), limite, offset)
        )
    else:
        cur.execute(
            "SELECT * FROM despesa_agregada ORDER BY valor_despesas DESC LIMIT %s OFFSET %s",
            (limite, offset)
        )
    
    despesas = cur.fetchall()
    cur.close()
    conn.close()
    
    return {"data": despesas, "limite": limite, "offset": offset}


@app.get("/despesas/top10")
def top10_despesas():
    """
    Retorna as 10 operadoras com maiores despesas agregadas.
    """
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute(
        "SELECT * FROM despesa_agregada ORDER BY valor_despesas DESC LIMIT 10"
    )
    
    despesas = cur.fetchall()
    cur.close()
    conn.close()
    
    return {"data": despesas}
