-- 1. PRINCIPAIS FORNECEDORES EM 2025
SELECT
    p.no_pais,
    ROUND(SUM(i.vl_fob) / 1000000000.0, 2) AS importacoes_usd_bilhoes,
    ROUND(100.0 * SUM(i.vl_fob)/ SUM(SUM(i.vl_fob)) OVER (),2) AS participacao_pct
FROM importacoes i
INNER JOIN ncm n ON i.co_ncm = n.co_ncm
INNER JOIN categorias_tecnologia c ON n.co_sh6 = c.co_sh6
INNER JOIN paises p ON i.co_pais = p.co_pais
WHERE i.co_ano = 2025
GROUP BY p.no_pais
ORDER BY importacoes_usd_bilhoes DESC
LIMIT 10;


-- 2. PRINCIPAL FORNECEDOR DE CADA CATEGORIA EM 2025
WITH fornecedores AS (
    SELECT
        c.categoria,
        p.no_pais,
        SUM(i.vl_fob) AS importacoes
    FROM importacoes i
    INNER JOIN ncm n ON i.co_ncm = n.co_ncm
    INNER JOIN categorias_tecnologia c ON n.co_sh6 = c.co_sh6
    INNER JOIN paises p ON i.co_pais = p.co_pais
    WHERE i.co_ano = 2025
    GROUP BY c.categoria, p.no_pais
),
ranking AS (
    SELECT
        categoria,
        no_pais,
        importacoes,
        SUM(importacoes) OVER (PARTITION BY categoria) AS total_categoria,
        ROW_NUMBER() OVER (PARTITION BY categoria ORDER BY importacoes DESC) AS posicao
    FROM fornecedores
)
SELECT
    categoria,
    no_pais AS principal_fornecedor,
    ROUND(importacoes / 1000000000.0, 2) AS importacoes_usd_bilhoes,
    ROUND(100.0 * importacoes / total_categoria, 2) AS participacao_categoria_pct
FROM ranking
WHERE posicao = 1
ORDER BY importacoes_usd_bilhoes DESC;


-- 3. CINCO PRINCIPAIS FORNECEDORES DE CADA CATEGORIA EM 2025
WITH fornecedores AS (
    SELECT
        c.categoria,
        p.no_pais,
        SUM(i.vl_fob) AS importacoes
    FROM importacoes i
    INNER JOIN ncm n ON i.co_ncm = n.co_ncm
    INNER JOIN categorias_tecnologia c ON n.co_sh6 = c.co_sh6
    INNER JOIN paises p ON i.co_pais = p.co_pais
    WHERE i.co_ano = 2025
    GROUP BY c.categoria, p.no_pais
),
ranking AS (
    SELECT
        categoria,
        no_pais,
        importacoes,
        SUM(importacoes) OVER (PARTITION BY categoria) AS total_categoria,
        ROW_NUMBER() OVER (PARTITION BY categoria ORDER BY importacoes DESC) AS posicao
    FROM fornecedores
)
SELECT
    categoria,
    posicao,
    no_pais,
    ROUND(importacoes / 1000000000.0, 2) AS importacoes_usd_bilhoes,
    ROUND(100.0 * importacoes / total_categoria, 2) AS participacao_categoria_pct
FROM ranking
WHERE posicao <= 5
ORDER BY categoria, posicao;


-- 4. COMO MUDOU O PRINCIPAL FORNECEDOR DE CADA CATEGORIA?
WITH fornecedores AS (
    SELECT
        i.co_ano,
        c.categoria,
        p.no_pais,
        SUM(i.vl_fob) AS importacoes
    FROM importacoes i
    INNER JOIN ncm n ON i.co_ncm = n.co_ncm
    INNER JOIN categorias_tecnologia c ON n.co_sh6 = c.co_sh6
    INNER JOIN paises p ON i.co_pais = p.co_pais
    GROUP BY i.co_ano, c.categoria, p.no_pais
),
ranking AS (
    SELECT
        co_ano,
        categoria,
        no_pais,
        importacoes,
        SUM(importacoes) OVER (
            PARTITION BY co_ano, categoria
        ) AS total_categoria,
        ROW_NUMBER() OVER (
            PARTITION BY co_ano, categoria
            ORDER BY importacoes DESC
        ) AS posicao
    FROM fornecedores
)
SELECT
    co_ano,
    categoria,
    no_pais AS principal_fornecedor,
    ROUND(importacoes / 1000000000.0, 2) AS importacoes_usd_bilhoes,
    ROUND(100.0 * importacoes / total_categoria, 2) AS participacao_categoria_pct
FROM ranking
WHERE posicao = 1
ORDER BY co_ano, categoria;