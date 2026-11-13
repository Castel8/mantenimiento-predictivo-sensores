-- Ejercicio 1: filas totales, fallas totales y tasa de falla en porcentaje
-- Pista: COUNT(*), SUM(falla) y 100.0 * SUM(falla) / COUNT(*).
-- El 100.0 (con decimal) evita que SQLite haga división entera y devuelva 0.
-- Redondea la tasa a 2 decimales con ROUND(valor, 2).

SELECT
    COUNT(*) AS filas,
    SUM(falla) AS fallas,
    ROUND(100.0 * SUM(falla) / COUNT(*), 2) AS tasa_pct
FROM lecturas;


-- Ejercicio 2: promedio de torque y de temperatura de proceso por tipo
-- Pista: SELECT tipo, AVG(...) ... FROM lecturas GROUP BY tipo.
-- GROUP BY separa las filas en grupos y calcula una cifra por cada grupo.

SELECT tipo,
       ROUND(AVG(torque_nm), 2) AS torque_prom,
       ROUND(AVG(temp_proceso_k), 2) AS temp_proceso_prom
FROM lecturas
GROUP BY tipo;


-- Ejercicio 3: tipos cuya tasa de falla supera la tasa global
-- Pista: GROUP BY tipo y luego HAVING AVG(falla) > (una subconsulta que calcule AVG(falla) de toda la tabla).
-- WHERE filtra filas antes de agrupar; HAVING filtra los grupos ya calculados.

SELECT tipo, ROUND(AVG(falla), 4) AS tasa
FROM lecturas
GROUP BY tipo
HAVING AVG(falla) > (SELECT AVG(falla) FROM lecturas);

-- Ejercicio 4: las 10 lecturas con mayor desgaste de herramienta
-- Pista: muestra udi, tipo, desgaste_min y falla; ORDER BY desgaste_min DESC y LIMIT 10.

SELECT udi, tipo, desgaste_min, falla
FROM lecturas
ORDER BY desgaste_min DESC
LIMIT 10;