# mantenimiento-predictivo-sensores

## Problema
Predecir si una máquina fallará a partir de lecturas de sensores de proceso (temperatura, velocidad de rotación, torque y desgaste de herramienta).

## Datos
- Fuente: AI4I 2020 Predictive Maintenance Dataset, UCI Machine Learning Repository (Matzka, 2020). DOI: 10.24432/C5HS5C. Licencia CC BY 4.0.
- Es un conjunto **sintético** que imita datos industriales reales. 10 000 filas, 14 columnas.
- Archivo original sin modificar: `data/raw/ai4i2020.csv`.

| Columna | Descripción |
|---|---|
| UDI | Identificador único (1 a 10 000) |
| Product ID | Calidad del producto (L, M, H) y número de serie |
| Type | Calidad: L (baja), M (media), H (alta) |
| Air temperature [K] | Temperatura del aire |
| Process temperature [K] | Temperatura del proceso |
| Rotational speed [rpm] | Velocidad de rotación |
| Torque [Nm] | Torque |
| Tool wear [min] | Desgaste de la herramienta |
| Machine failure | **Objetivo**: 1 si hubo falla, 0 si no |
| TWF, HDF, PWF, OSF, RNF | Modos de falla (desgaste, disipación de calor, potencia, sobrecarga, aleatoria) |

Nota: `Machine failure` vale 1 cuando ocurre cualquiera de los cinco modos de falla, así que esas cinco columnas **no se usarán como variables de entrada** del modelo (filtrarían la respuesta).
Calidad de los datos: 0 nulos y 0 duplicados. Hay 27 filas (0.27 %) con inconsistencias de origen: 9 con falla sin ningún modo activo y 18 con falla aleatoria (RNF) sin falla registrada. Se conservaron y no afectan al modelo porque la etiqueta es `Machine failure`.
