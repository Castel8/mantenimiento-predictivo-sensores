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


-- Verificación: columnas de las tablas
SELECT 'lecturas' AS tabla, name FROM pragma_table_info('lecturas')
UNION ALL
SELECT 'tipos', name FROM pragma_table_info('tipos');

-- Ejercicio 5: nombre de calidad y tasa de falla por tipo
SELECT t.calidad,
       l.tipo,
       COUNT(*) AS filas,
       ROUND(AVG(l.falla), 4) AS tasa
FROM lecturas l
JOIN tipos t ON t.tipo = l.tipo
GROUP BY t.calidad, l.tipo
ORDER BY tasa DESC;

-- Ejercicio 6: clasificar rpm en bajo, medio y alto y contar fallas por categoría
SELECT CASE
           WHEN rpm < 1400 THEN 'bajo'
           WHEN rpm <= 1700 THEN 'medio'
           ELSE 'alto'
       END AS categoria_rpm,
       COUNT(*) AS filas,
       SUM(falla) AS fallas,
       ROUND(100.0 * SUM(falla) / COUNT(*), 2) AS tasa_pct
FROM lecturas
GROUP BY categoria_rpm
ORDER BY tasa_pct DESC;

-- Ejercicio 7: lecturas con torque mayor al promedio de su propio tipo
SELECT l.udi, l.tipo, l.torque_nm,
       ROUND((SELECT AVG(torque_nm) FROM lecturas WHERE tipo = l.tipo), 2) AS torque_prom_tipo
FROM lecturas l
WHERE l.torque_nm > (SELECT AVG(torque_nm) FROM lecturas WHERE tipo = l.tipo)
ORDER BY l.torque_nm DESC
LIMIT 15;

-- Ejercicio 8: tasa de falla por tipo con ranking (CTE)
WITH tasas AS (
    SELECT tipo,
           COUNT(*) AS filas,
           SUM(falla) AS fallas,
           ROUND(100.0 * SUM(falla) / COUNT(*), 2) AS tasa_pct
    FROM lecturas
    GROUP BY tipo
)
SELECT tipo, filas, fallas, tasa_pct,
       RANK() OVER (ORDER BY tasa_pct DESC) AS ranking
FROM tasas;

-- Ejercicio 9a: ranking de torque dentro de cada tipo (top 3 por tipo)
WITH ranking AS (
    SELECT udi, tipo, torque_nm,
           RANK() OVER (PARTITION BY tipo ORDER BY torque_nm DESC) AS rank_torque
    FROM lecturas
)
SELECT udi, tipo, torque_nm, rank_torque
FROM ranking
WHERE rank_torque <= 3
ORDER BY tipo, rank_torque;

-- Ejercicio 9b: promedio móvil de 50 lecturas de temperatura de proceso
-- (se muestran las filas 46 a 55 para ver cómo la ventana se completa en la 50)
WITH movil AS (
    SELECT udi, temp_proceso_k,
           AVG(temp_proceso_k) OVER (
               ORDER BY udi
               ROWS BETWEEN 49 PRECEDING AND CURRENT ROW
           ) AS prom_movil_50
    FROM lecturas
)
SELECT udi, temp_proceso_k, ROUND(prom_movil_50, 3) AS prom_movil_50
FROM movil
WHERE udi BETWEEN 46 AND 55
ORDER BY udi;

-- Ejercicio 10: diferencia de desgaste frente a la lectura anterior
SELECT udi, tipo, desgaste_min,
       LAG(desgaste_min) OVER (ORDER BY udi) AS desgaste_anterior,
       desgaste_min - LAG(desgaste_min) OVER (ORDER BY udi) AS diferencia
FROM lecturas
ORDER BY udi
LIMIT 15;