
-- 1. COMPARAÇÃO POR CATEGORIA: 2010 X 2025
WITH imp AS (
    SELECT
        i.co_ano,
        c.categoria,
        SUM(i.vl_fob) AS importacoes
    FROM importacoes i
    INNER JOIN ncm n ON i.co_ncm = n.co_ncm
    INNER JOIN categorias_tecnologia c ON n.co_sh6 = c.co_sh6
    WHERE i.co_ano IN (2010, 2025)
    GROUP BY
        i.co_ano,
        c.categoria
),
exp AS (
    SELECT
        e.co_ano,
        c.categoria,
        SUM(e.vl_fob) AS exportacoes
    FROM exportacoes e
    INNER JOIN ncm n ON e.co_ncm = n.co_ncm
    INNER JOIN categorias_tecnologia c ON n.co_sh6 = c.co_sh6
    WHERE e.co_ano IN (2010, 2025)
    GROUP BY
        e.co_ano,
        c.categoria
),
balanca AS (
    SELECT
        i.co_ano,
        i.categoria,
        i.importacoes,
        e.exportacoes,
        e.exportacoes - i.importacoes AS saldo
    FROM imp i
    INNER JOIN exp e ON i.co_ano = e.co_ano AND i.categoria = e.categoria
)
SELECT
    categoria,
    ROUND(MAX(CASE WHEN co_ano = 2010 THEN importacoes END) / 1000000000.0, 2) AS importacoes_2010_usd_bilhoes,
    ROUND(MAX(CASE WHEN co_ano = 2025 THEN importacoes END) / 1000000000.0, 2) AS importacoes_2025_usd_bilhoes,
    ROUND(MAX(CASE WHEN co_ano = 2010 THEN exportacoes END) / 1000000000.0, 2) AS exportacoes_2010_usd_bilhoes,
    ROUND(MAX(CASE WHEN co_ano = 2025 THEN exportacoes END) / 1000000000.0, 2) AS exportacoes_2025_usd_bilhoes,
    ROUND(MAX(CASE WHEN co_ano = 2010 THEN saldo END) / 1000000000.0, 2) AS saldo_2010_usd_bilhoes,
    ROUND(MAX(CASE WHEN co_ano = 2025 THEN saldo END) / 1000000000.0, 2) AS saldo_2025_usd_bilhoes
FROM balanca
GROUP BY
    categoria
ORDER BY
    importacoes_2025_usd_bilhoes DESC;


-- 2. COMPARAÇÃO DO TOTAL DE BENS TIC: 2010 X 2025
WITH imp AS (
    SELECT
        i.co_ano,
        SUM(i.vl_fob) AS importacoes
    FROM importacoes i
    INNER JOIN ncm n ON i.co_ncm = n.co_ncm
    INNER JOIN categorias_tecnologia c ON n.co_sh6 = c.co_sh6
    WHERE i.co_ano IN (2010, 2025)
    GROUP BY
        i.co_ano
),
exp AS (
    SELECT
        e.co_ano,
        SUM(e.vl_fob) AS exportacoes
    FROM exportacoes e
    INNER JOIN ncm n ON e.co_ncm = n.co_ncm
    INNER JOIN categorias_tecnologia c ON n.co_sh6 = c.co_sh6
    WHERE e.co_ano IN (2010, 2025)
    GROUP BY
        e.co_ano
)
SELECT
    i.co_ano,
    ROUND(i.importacoes / 1000000000.0, 2) AS importacoes_usd_bilhoes,
    ROUND(e.exportacoes / 1000000000.0, 2) AS exportacoes_usd_bilhoes,
    ROUND((e.exportacoes - i.importacoes) / 1000000000.0, 2) AS saldo_usd_bilhoes
FROM imp i
INNER JOIN exp e ON i.co_ano = e.co_ano
ORDER BY
    i.co_ano;