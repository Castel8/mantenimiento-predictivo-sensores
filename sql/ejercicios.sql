-- Verificación 1: tamaño de la tabla y fallas totales
SELECT COUNT(*) AS filas, SUM(falla) AS fallas FROM lecturas;

-- Verificación 2: tabla de tipos de calidad
SELECT * FROM tipos;