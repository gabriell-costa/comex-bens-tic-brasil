-- 1. IMPORTAÇÕES POR CATEGORIA NO PERÍODO COMPLETO
SELECT
    c.categoria,
    ROUND(SUM(i.vl_fob) / 1000000000.0, 2) AS importacoes_usd_bilhoes
FROM importacoes i
INNER JOIN ncm n ON i.co_ncm = n.co_ncm
INNER JOIN categorias_tecnologia c ON n.co_sh6 = c.co_sh6
GROUP BY c.categoria
ORDER BY importacoes_usd_bilhoes DESC;


-- 2. IMPORTAÇÕES POR ANO E CATEGORIA
SELECT
    i.co_ano,
    c.categoria,
    ROUND(SUM(i.vl_fob) / 1000000000.0, 2) AS importacoes_usd_bilhoes
FROM importacoes i
INNER JOIN ncm n ON i.co_ncm = n.co_ncm
INNER JOIN categorias_tecnologia c ON n.co_sh6 = c.co_sh6
GROUP BY i.co_ano, c.categoria
ORDER BY i.co_ano, importacoes_usd_bilhoes DESC;


-- 3. QUANTIDADE DE CÓDIGOS TIC ENCONTRADOS POR ANO E CATEGORIA
SELECT
    i.co_ano,
    c.categoria,
    COUNT(DISTINCT c.co_sh6) AS codigos_encontrados
FROM importacoes i
INNER JOIN ncm n ON i.co_ncm = n.co_ncm
INNER JOIN categorias_tecnologia c ON n.co_sh6 = c.co_sh6
GROUP BY i.co_ano, c.categoria
ORDER BY i.co_ano, c.categoria;

