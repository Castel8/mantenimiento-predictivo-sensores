import io
import urllib.request
import zipfile
from pathlib import Path
import pandas as pd

RAIZ = Path(__file__).resolve().parent.parent
RAW = RAIZ / "data" / "raw"
CSV = RAW / "ai4i2020.csv"
URL = "https://archive.ics.uci.edu/static/public/601/ai4i+2020+predictive+maintenance+dataset.zip"


def descargar():
    RAW.mkdir(parents=True, exist_ok=True)
    if CSV.exists():
        print("El archivo ya existe en data/raw, no se descarga de nuevo.")
        return
    peticion = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(peticion, timeout=60) as respuesta:
        contenido = respuesta.read()
    with zipfile.ZipFile(io.BytesIO(contenido)) as z:
        nombre = [n for n in z.namelist() if n.lower().endswith(".csv")][0]
        CSV.write_bytes(z.read(nombre))
    print(f"Descargado en {CSV}")


if __name__ == "__main__":
    descargar()
    df = pd.read_csv(CSV)
    print("\nFilas y columnas:", df.shape)
    print("\nColumnas y tipos:")
    print(df.dtypes)
    print("\nPrimeras filas:")
    print(df.head(3).to_string())
    print("\nValores nulos en total:", int(df.isna().sum().sum()))
    print("\nMachine failure (0 = sin falla, 1 = falla):")
    print(df["Machine failure"].value_counts())