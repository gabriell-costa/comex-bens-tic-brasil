-- 1. BALANÇA COMERCIAL POR ANO E CATEGORIA
WITH imp AS (
    SELECT
        i.co_ano,
        c.categoria,
        SUM(i.vl_fob) AS importacoes
    FROM importacoes i
    INNER JOIN ncm n ON i.co_ncm = n.co_ncm
    INNER JOIN categorias_tecnologia c ON n.co_sh6 = c.co_sh6
    GROUP BY i.co_ano, c.categoria
),
exp AS (
    SELECT
        e.co_ano,
        c.categoria,
        SUM(e.vl_fob) AS exportacoes
    FROM exportacoes e
    INNER JOIN ncm n ON e.co_ncm = n.co_ncm
    INNER JOIN categorias_tecnologia c ON n.co_sh6 = c.co_sh6
    GROUP BY e.co_ano, c.categoria
)
SELECT
    i.co_ano,
    i.categoria,
    ROUND(i.importacoes / 1000000000.0, 2) AS importacoes_usd_bilhoes,
    ROUND(e.exportacoes / 1000000000.0, 2) AS exportacoes_usd_bilhoes,
    ROUND((e.exportacoes - i.importacoes) / 1000000000.0, 2) AS saldo_usd_bilhoes,
    ROUND(i.importacoes / NULLIF(e.exportacoes, 0), 2) AS razao_importacao_exportacao
FROM imp i
INNER JOIN exp e ON i.co_ano = e.co_ano AND i.categoria = e.categoria
ORDER BY i.co_ano, i.categoria;


-- 2. BALANÇA COMERCIAL TOTAL DOS BENS TIC POR ANO
WITH imp AS (
    SELECT
        i.co_ano,
        SUM(i.vl_fob) AS importacoes
    FROM importacoes i
    INNER JOIN ncm n ON i.co_ncm = n.co_ncm
    INNER JOIN categorias_tecnologia c ON n.co_sh6 = c.co_sh6
    GROUP BY i.co_ano
),
exp AS (
    SELECT
        e.co_ano,
        SUM(e.vl_fob) AS exportacoes
    FROM exportacoes e
    INNER JOIN ncm n ON e.co_ncm = n.co_ncm
    INNER JOIN categorias_tecnologia c ON n.co_sh6 = c.co_sh6
    GROUP BY e.co_ano
)
SELECT
    i.co_ano,
    ROUND(i.importacoes / 1000000000.0, 2) AS importacoes_usd_bilhoes,
    ROUND(e.exportacoes / 1000000000.0, 2) AS exportacoes_usd_bilhoes,
    ROUND((e.exportacoes - i.importacoes) / 1000000000.0, 2) AS saldo_usd_bilhoes,
    ROUND(i.importacoes / NULLIF(e.exportacoes, 0), 2) AS razao_importacao_exportacao
FROM imp i
INNER JOIN exp e ON i.co_ano = e.co_ano
ORDER BY i.co_ano;


-- 3. BALANÇA COMERCIAL ACUMULADA POR CATEGORIA — 2010 A 2025
WITH imp AS (
    SELECT
        c.categoria,
        SUM(i.vl_fob) AS importacoes
    FROM importacoes i
    INNER JOIN ncm n ON i.co_ncm = n.co_ncm
    INNER JOIN categorias_tecnologia c ON n.co_sh6 = c.co_sh6
    GROUP BY c.categoria
),
exp AS (
    SELECT
        c.categoria,
        SUM(e.vl_fob) AS exportacoes
    FROM exportacoes e
    INNER JOIN ncm n ON e.co_ncm = n.co_ncm
    INNER JOIN categorias_tecnologia c ON n.co_sh6 = c.co_sh6
    GROUP BY c.categoria
)
SELECT
    i.categoria,
    ROUND(i.importacoes / 1000000000.0, 2) AS importacoes_usd_bilhoes,
    ROUND(e.exportacoes / 1000000000.0, 2) AS exportacoes_usd_bilhoes,
    ROUND((e.exportacoes - i.importacoes) / 1000000000.0, 2) AS saldo_usd_bilhoes,
    ROUND(i.importacoes / NULLIF(e.exportacoes, 0), 2) AS razao_importacao_exportacao
FROM imp i
INNER JOIN exp e ON i.categoria = e.categoria
ORDER BY saldo_usd_bilhoes;