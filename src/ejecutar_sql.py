import sqlite3
import sys
from pathlib import Path
import pandas as pd

RAIZ = Path(__file__).resolve().parent.parent
DB = RAIZ / "data" / "ai4i.db"
ARCHIVO = Path(sys.argv[1]) if len(sys.argv) > 1 else RAIZ / "sql" / "ejercicios.sql"

con = sqlite3.connect(DB)
texto = ARCHIVO.read_text(encoding="utf-8")
for bloque in texto.split(";"):
    sentencia = bloque.strip()
    lineas = sentencia.splitlines()
    if not sentencia or all(l.strip().startswith("--") for l in lineas):
        continue
    titulo = next((l for l in lineas if l.strip().startswith("--")), "")
    print("\n" + titulo)
    try:
        print(pd.read_sql(sentencia, con).to_string(index=False))
    except Exception as e:
        print("ERROR:", e)
con.close()