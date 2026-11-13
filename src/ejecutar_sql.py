import sqlite3
import sys
from pathlib import Path
import pandas as pd

RAIZ = Path(__file__).resolve().parent.parent
DB = RAIZ / "data" / "ai4i.db"
ARCHIVO = Path(sys.argv[1]) if len(sys.argv) > 1 else RAIZ / "sql" / "ejercicios.sql"

con = sqlite3.connect(DB)
titulo = ""
sentencia = []
for linea in ARCHIVO.read_text(encoding="utf-8").splitlines():
    s = linea.strip()
    if s.startswith("--"):
        if not sentencia and not titulo:
            titulo = s
        continue
    if not s:
        continue
    sentencia.append(linea)
    if s.endswith(";"):
        consulta = "\n".join(sentencia).rstrip().rstrip(";")
        print("\n" + titulo)
        try:
            print(pd.read_sql(consulta, con).to_string(index=False))
        except Exception as e:
            print("ERROR:", e)
        titulo = ""
        sentencia = []
con.close()