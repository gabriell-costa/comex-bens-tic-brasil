-- 1. PRODUTOS TIC MAIS IMPORTADOS
WITH produtos AS (
    SELECT
        c.categoria,
        i.co_ncm,
        n.no_ncm_por AS produto,
        SUM(i.vl_fob) AS importacoes
    FROM importacoes i
    INNER JOIN ncm n ON i.co_ncm = n.co_ncm
    INNER JOIN categorias_tecnologia c ON n.co_sh6 = c.co_sh6
    WHERE i.co_ano = 2025
    GROUP BY c.categoria, i.co_ncm, n.no_ncm_por
)
SELECT
    categoria,
    co_ncm,
    produto,
    ROUND(importacoes / 1000000.0, 2) AS importacoes_usd_milhoes
FROM produtos
ORDER BY importacoes DESC
LIMIT 20;


-- 2. PRODUTOS TIC COM MAIOR DÉFICIT COMERCIAL

WITH imp AS (
    SELECT
        i.co_ncm,
        SUM(i.vl_fob) AS importacoes
    FROM importacoes i
    INNER JOIN ncm n ON i.co_ncm = n.co_ncm
    INNER JOIN categorias_tecnologia c ON n.co_sh6 = c.co_sh6
    WHERE i.co_ano = 2025
    GROUP BY
        i.co_ncm
),
exp AS (
    SELECT
        e.co_ncm,
        SUM(e.vl_fob) AS exportacoes
    FROM exportacoes e
    INNER JOIN ncm n ON e.co_ncm = n.co_ncm
    INNER JOIN categorias_tecnologia c ON n.co_sh6 = c.co_sh6
    WHERE e.co_ano = 2025
    GROUP BY
        e.co_ncm
)
SELECT
    c.categoria,
    n.co_ncm,
    n.no_ncm_por AS produto,
    ROUND(COALESCE(i.importacoes, 0) / 1000000.0, 2) AS importacoes_usd_milhoes,
    ROUND(COALESCE(e.exportacoes, 0) / 1000000.0, 2) AS exportacoes_usd_milhoes,
    ROUND(COALESCE(e.exportacoes, 0) - COALESCE(i.importacoes, 0)) / 1000000.0, 2) AS saldo_usd_milhoes
FROM ncm n
INNER JOIN categorias_tecnologia c ON n.co_sh6 = c.co_sh6
LEFT JOIN imp i ON n.co_ncm = i.co_ncm
LEFT JOIN exp e ON n.co_ncm = e.co_ncm
WHERE (i.co_ncm IS NOT NULL OR e.co_ncm IS NOT NULL)
ORDER BY saldo_usd_milhoes
LIMIT 20;