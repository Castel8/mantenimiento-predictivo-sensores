# mantenimiento-predictivo-sensores

# Predicción de fallas de máquinas con sensores (AI4I 2020)

Proyecto de punta a punta: exploración de datos, modelo de machine learning y dashboard en Streamlit para predecir fallas en una máquina a partir de lecturas de sensores.

## Problema
En manufactura, una falla inesperada detiene la producción. El objetivo es predecir si una máquina fallará según sus lecturas de sensores, priorizando detectar fallas reales (recall) sin generar demasiadas falsas alarmas.

## Datos
- **Fuente:** AI4I 2020 Predictive Maintenance Dataset (UCI Machine Learning Repository / Kaggle). Es un conjunto **sintético** que imita datos reales de mantenimiento predictivo.
- **Tamaño:** 10 000 filas, 14 columnas originales.
- **Archivo original (intacto):** `data/raw/ai4i2020.csv`
- **Archivo limpio:** `data/clean/ai4i2020_clean.csv`

### Diccionario de columnas
| Columna original | Nombre en `clean` | Significado |
|---|---|---|
| UDI | udi | Identificador de la fila (1 a 10000) |
| Product ID | product_id | Identificador del producto; la primera letra es el tipo |
| Type | type | Calidad del producto: L (baja), M (media), H (alta) |
| Air temperature [K] | air_temp_k | Temperatura del aire, en kelvin |
| Process temperature [K] | process_temp_k | Temperatura del proceso, en kelvin |
| Rotational speed [rpm] | rpm | Velocidad de rotación |
| Torque [Nm] | torque_nm | Torque, en newton-metro |
| Tool wear [min] | tool_wear_min | Minutos de desgaste de la herramienta |
| Machine failure | machine_failure | **Variable objetivo**: 1 si hubo falla, 0 si no |
| TWF | twf | Falla por desgaste de herramienta |
| HDF | hdf | Falla por disipación de calor (rpm baja y poca diferencia de temperatura) |
| PWF | pwf | Falla de potencia (potencia fuera de 3500–9000 W) |
| OSF | osf | Falla por sobreesfuerzo (desgaste × torque sobre un umbral según el tipo) |
| RNF | rnf | Falla aleatoria (0.1 % de probabilidad) |
| (nueva) | etiqueta_inconsistente | 1 si `machine_failure` no coincide con los 5 modos de falla |

## Limpieza y exploración
- Sin nulos ni duplicados; tipos de dato correctos.
- **Desbalance:** solo 339 de 10 000 filas (3.4 %) son fallas. Por eso se evalúa con precision, recall y F1, no solo accuracy.
- **Inconsistencias:** 27 filas (0.27 %) donde la etiqueta no coincide con los modos de falla (9 con falla sin modo activo y 18 con `RNF = 1` sin falla). Se conservan y se marcan en `etiqueta_inconsistente`.
- **Outliers (regla del IQR):** se conservan, porque son lecturas reales y muchas coinciden con fallas.
- **Hallazgos:**
  - Las fallas aparecen en los extremos de torque y de velocidad, no en valores centrales (relación no lineal).
  - Torque y rpm tienen correlación de -0.88; temperatura del aire y del proceso, 0.88.
  - La correlación lineal con la falla es baja (torque 0.19, desgaste 0.11), por lo que se esperan mejores resultados con modelos basados en árboles.

### Gráficos
![Balance de clases](reports/figures/1_balance_clases.png)
![Torque y velocidad por falla](reports/figures/2_3_torque_velocidad_por_falla.png)
![Correlaciones](reports/figures/4_correlaciones.png)

## Modelo y resultados
*(Pendiente: se completa con el paso 4 y 5.)*

## Dashboard
*(Pendiente: capturas y enlace al paso 6.)*

## Cómo ejecutarlo
*(Pendiente: se completa con el paso 7.)*

## Estructura del repositorio
```
data/raw      datos originales sin modificar
data/clean    datos limpios
notebooks/    exploración y modelo
src/          código reutilizable
app/          dashboard en Streamlit
sql/          consultas
reports/figures/  gráficos
```
