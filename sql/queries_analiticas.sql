USE clima_energia_global;

-- ══════════════════════════════════════════════════════
-- QUERIES ANALÍTICAS — PROYECTO CLIMA Y ENERGÍA
-- Autor: Miguel Sierra
-- ══════════════════════════════════════════════════════


-- ── Q1. Total de registros por país ───────────────────
-- Verificación de integridad del dataset
SELECT
    pais,
    region,
    COUNT(*)            AS total_registros,
    MIN(fecha)          AS fecha_inicio,
    MAX(fecha)          AS fecha_fin
FROM registros_clima_energia
GROUP BY pais, region
ORDER BY region, pais;


-- ── Q2. Temperatura promedio por país ─────────────────
-- ¿Qué países tienen mayor temperatura promedio?
SELECT
    pais,
    region,
    ROUND(AVG(temperatura_promedio), 2)  AS temp_promedio,
    ROUND(MIN(temperatura_promedio), 2)  AS temp_minima,
    ROUND(MAX(temperatura_promedio), 2)  AS temp_maxima,
    ROUND(STDDEV(temperatura_promedio), 2) AS temp_desviacion
FROM registros_clima_energia
GROUP BY pais, region
ORDER BY temp_promedio DESC;


-- ── Q3. Temperatura promedio por región ───────────────
SELECT
    region,
    ROUND(AVG(temperatura_promedio), 2)  AS temp_promedio,
    ROUND(MIN(temperatura_promedio), 2)  AS temp_minima,
    ROUND(MAX(temperatura_promedio), 2)  AS temp_maxima
FROM registros_clima_energia
GROUP BY region
ORDER BY temp_promedio DESC;


-- ── Q4. Emisiones de CO₂ promedio por país ────────────
-- ¿Qué países emiten más CO₂?
SELECT
    pais,
    region,
    ROUND(AVG(emision_co2), 2)   AS co2_promedio,
    ROUND(MIN(emision_co2), 2)   AS co2_minimo,
    ROUND(MAX(emision_co2), 2)   AS co2_maximo,
    ROUND(STDDEV(emision_co2), 2) AS co2_desviacion
FROM registros_clima_energia
GROUP BY pais, region
ORDER BY co2_promedio DESC;


-- ── Q5. Evolución anual de CO₂ por región ─────────────
-- ¿Está bajando el CO₂ con el tiempo?
SELECT
    region,
    YEAR(fecha)                  AS anio,
    ROUND(AVG(emision_co2), 2)   AS co2_promedio,
    COUNT(*)                     AS registros
FROM registros_clima_energia
GROUP BY region, YEAR(fecha)
ORDER BY region, anio;


-- ── Q6. Ranking de energías renovables ────────────────
-- ¿Qué países lideran en renovables?
SELECT
    pais,
    region,
    ROUND(AVG(participacion_renovable), 2)  AS renovable_promedio,
    ROUND(MIN(participacion_renovable), 2)  AS renovable_minimo,
    ROUND(MAX(participacion_renovable), 2)  AS renovable_maximo
FROM registros_clima_energia
GROUP BY pais, region
ORDER BY renovable_promedio DESC;


-- ── Q7. Países por encima del promedio global ─────────
-- en participación renovable
SELECT
    pais,
    region,
    ROUND(AVG(participacion_renovable), 2) AS renovable_promedio,
    ROUND(
        (SELECT AVG(participacion_renovable)
         FROM registros_clima_energia), 2
    ) AS promedio_global
FROM registros_clima_energia
GROUP BY pais, region
HAVING renovable_promedio >
    (SELECT AVG(participacion_renovable)
     FROM registros_clima_energia)
ORDER BY renovable_promedio DESC;


-- ── Q8. Consumo energético promedio por región ────────
SELECT
    region,
    ROUND(AVG(consumo_energetico), 2)    AS consumo_promedio,
    ROUND(AVG(precio_energia), 2)        AS precio_promedio,
    ROUND(AVG(emision_co2), 2)           AS co2_promedio,
    ROUND(AVG(participacion_renovable), 2) AS renovable_promedio
FROM registros_clima_energia
GROUP BY region
ORDER BY consumo_promedio DESC;


-- ── Q9. Relación CO₂ vs consumo energético ────────────
-- Los 10 registros con mayor CO₂ y su consumo asociado
SELECT
    pais,
    fecha,
    ROUND(emision_co2, 2)        AS co2,
    ROUND(consumo_energetico, 2) AS consumo,
    ROUND(precio_energia, 2)     AS precio
FROM registros_clima_energia
ORDER BY emision_co2 DESC
LIMIT 10;


-- ── Q10. Precio de energía promedio por país ──────────
SELECT
    pais,
    region,
    ROUND(AVG(precio_energia), 2)   AS precio_promedio,
    ROUND(MIN(precio_energia), 2)   AS precio_minimo,
    ROUND(MAX(precio_energia), 2)   AS precio_maximo
FROM registros_clima_energia
GROUP BY pais, region
ORDER BY precio_promedio DESC;


-- ── Q11. Evolución anual de renovables ────────────────
-- ¿Está creciendo la participación renovable?
SELECT
    YEAR(fecha)                             AS anio,
    ROUND(AVG(participacion_renovable), 2)  AS renovable_promedio,
    ROUND(AVG(emision_co2), 2)              AS co2_promedio,
    ROUND(AVG(consumo_energetico), 2)       AS consumo_promedio
FROM registros_clima_energia
GROUP BY YEAR(fecha)
ORDER BY anio;


-- ── Q12. Top 5 países mejor desempeño ambiental ───────
-- Mayor renovable + menor CO₂
SELECT
    pais,
    region,
    ROUND(AVG(participacion_renovable), 2) AS renovable_promedio,
    ROUND(AVG(emision_co2), 2)             AS co2_promedio,
    ROUND(AVG(precio_energia), 2)          AS precio_promedio,
    ROUND(
        AVG(participacion_renovable) /
        AVG(emision_co2) * 100, 4
    ) AS indice_ambiental
FROM registros_clima_energia
GROUP BY pais, region
ORDER BY indice_ambiental DESC
LIMIT 5;


-- ── Q13. Resumen ejecutivo global ─────────────────────
SELECT
    COUNT(DISTINCT pais)                        AS total_paises,
    COUNT(DISTINCT YEAR(fecha))                 AS total_anios,
    COUNT(*)                                    AS total_registros,
    ROUND(AVG(temperatura_promedio), 2)         AS temp_global_promedio,
    ROUND(AVG(emision_co2), 2)                  AS co2_global_promedio,
    ROUND(AVG(participacion_renovable), 2)      AS renovable_global_promedio,
    ROUND(AVG(consumo_energetico), 2)           AS consumo_global_promedio,
    ROUND(AVG(precio_energia), 2)               AS precio_global_promedio
FROM registros_clima_energia;