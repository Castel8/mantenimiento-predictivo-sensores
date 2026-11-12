from pathlib import Path
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

RAIZ = Path(__file__).resolve().parent.parent
COLORES = {0: "#4C72B0", 1: "#C44E52"}

st.set_page_config(page_title="Fallas de máquinas", layout="wide")


@st.cache_data
def cargar_datos():
    return pd.read_csv(RAIZ / "data" / "clean" / "ai4i2020_clean.csv")


@st.cache_resource
def cargar_modelo():
    return joblib.load(RAIZ / "models" / "modelo_gb.joblib")


df = cargar_datos()
modelo = cargar_modelo()

st.title("Predicción de fallas de máquinas")
st.caption("Dataset AI4I 2020 (sintético) · Modelo: Gradient Boosting")

tab1, tab2 = st.tabs(["📊 Exploración", "🔮 Simulador"])

# ---------- Pestaña 1: exploración con filtros ----------
with tab1:
    st.sidebar.header("Filtros")
    tipos = st.sidebar.multiselect("Tipo de producto", ["L", "M", "H"], default=["L", "M", "H"])
    rpm_min, rpm_max = int(df.rpm.min()), int(df.rpm.max())
    rango_rpm = st.sidebar.slider("Velocidad (rpm)", rpm_min, rpm_max, (rpm_min, rpm_max))
    w_min, w_max = int(df.tool_wear_min.min()), int(df.tool_wear_min.max())
    rango_wear = st.sidebar.slider("Desgaste de herramienta (min)", w_min, w_max, (w_min, w_max))

    f = df[
        df["type"].isin(tipos)
        & df.rpm.between(*rango_rpm)
        & df.tool_wear_min.between(*rango_wear)
    ]

    tasa_global = df.machine_failure.mean()
    if len(f) == 0:
        st.warning("Ninguna lectura cumple los filtros.")
    else:
        tasa = f.machine_failure.mean()
        c1, c2, c3 = st.columns(3)
        c1.metric("Lecturas filtradas", f"{len(f):,}")
        c2.metric("Fallas", f"{int(f.machine_failure.sum()):,}")
        c3.metric("Tasa de falla", f"{tasa:.2%}", f"{(tasa - tasa_global) * 100:+.2f} pts vs global")

        variables = {
            "Torque [Nm]": "torque_nm", "Velocidad [rpm]": "rpm",
            "Desgaste [min]": "tool_wear_min", "Temp. aire [K]": "air_temp_k",
            "Temp. proceso [K]": "process_temp_k",
        }
        nombre = st.selectbox("Variable a graficar", list(variables))
        col = variables[nombre]

        fig, ax = plt.subplots(figsize=(8, 3.5))
        if f.machine_failure.nunique() > 1:
            sns.histplot(data=f, x=col, hue="machine_failure", bins=40, stat="density",
                         common_norm=False, palette=COLORES, ax=ax)
        else:
            sns.histplot(data=f, x=col, bins=40, ax=ax)
        ax.set_title(f"{nombre} según falla (0 = sin falla, 1 = falla)")
        st.pyplot(fig)

# ---------- Pestaña 2: simulador ----------
with tab2:
    st.subheader("Simulador de falla")
    st.write("Ajusta las lecturas y el modelo estima la probabilidad de falla.")

    c1, c2 = st.columns(2)
    with c1:
        tipo = st.selectbox("Tipo de producto", ["L", "M", "H"], index=1)
        air = st.slider("Temperatura del aire [K]", 295.0, 305.0, 300.0, 0.1)
        proc = st.slider("Temperatura del proceso [K]", 305.0, 314.0, 310.0, 0.1)
    with c2:
        rpm = st.slider("Velocidad [rpm]", 1150, 2900, 1500, 10)
        torque = st.slider("Torque [Nm]", 3.0, 77.0, 40.0, 0.5)
        desgaste = st.slider("Desgaste de herramienta [min]", 0, 253, 100)

    entrada = pd.DataFrame([{
        "air_temp_k": air, "process_temp_k": proc, "rpm": rpm,
        "torque_nm": torque, "tool_wear_min": desgaste,
        "power_w": torque * rpm * 2 * np.pi / 60,
        "temp_diff_k": proc - air, "type": tipo,
    }])

    prob = modelo.predict_proba(entrada)[0, 1]
    st.metric("Probabilidad de falla", f"{prob:.1%}")
    st.progress(float(prob))
    if prob >= 0.5:
        st.error("⚠️ Riesgo ALTO de falla: se recomienda revisar la máquina.")
    else:
        st.success("✅ Riesgo bajo de falla.")
    st.caption(f"Potencia calculada: {entrada.power_w[0]:,.0f} W · "
               f"Diferencia de temperatura: {proc - air:.1f} K")