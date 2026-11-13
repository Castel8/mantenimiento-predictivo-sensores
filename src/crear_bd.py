import sqlite3
from pathlib import Path
import pandas as pd

RAIZ = Path(__file__).resolve().parent.parent
CSV = RAIZ / "data" / "raw" / "ai4i2020.csv"
DB = RAIZ / "data" / "ai4i.db"

COLUMNAS = {
    "UDI": "udi",
    "Product ID": "product_id",
    "Type": "tipo",
    "Air temperature [K]": "temp_aire_k",
    "Process temperature [K]": "temp_proceso_k",
    "Rotational speed [rpm]": "rpm",
    "Torque [Nm]": "torque_nm",
    "Tool wear [min]": "desgaste_min",
    "Machine failure": "falla",
    "TWF": "twf",
    "HDF": "hdf",
    "PWF": "pwf",
    "OSF": "osf",
    "RNF": "rnf",
}

df = pd.read_csv(CSV).rename(columns=COLUMNAS)
tipos = pd.DataFrame({"tipo": ["L", "M", "H"], "calidad": ["Baja", "Media", "Alta"]})

con = sqlite3.connect(DB)
df.to_sql("lecturas", con, if_exists="replace", index=False)
tipos.to_sql("tipos", con, if_exists="replace", index=False)
con.commit()
con.close()
print(f"Base creada en {DB}")
print(f"Tabla lecturas: {len(df)} filas. Tabla tipos: {len(tipos)} filas.")