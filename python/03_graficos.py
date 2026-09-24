from pathlib import Path
import duckdb
import pandas as pd
import matplotlib.pyplot as plt

BASE_DIR = Path(__file__).resolve().parent.parent
BANCO = BASE_DIR / "dados" / "soberania_digital.duckdb"
PASTA_GRAFICOS = BASE_DIR / "graficos"

PASTA_GRAFICOS.mkdir(exist_ok=True)

con = duckdb.connect(str(BANCO), read_only=True)

NOMES_CATEGORIAS = {
    "componentes_eletronicos": "Componentes eletrônicos",
    "computadores_perifericos": "Computadores e periféricos",
    "eletronicos_consumo": "Eletrônicos de consumo",
    "equipamentos_comunicacao": "Equipamentos de comunicação",
    "outros_bens_ict": "Outros bens TIC"
}

# ============================================================
# 1. EVOLUÇÃO DAS IMPORTAÇÕES POR CATEGORIA
# ============================================================

query_importacoes = """
SELECT
    i.co_ano,
    c.categoria,
    SUM(i.vl_fob) / 1000000000.0 AS importacoes_usd_bilhoes
FROM importacoes i
INNER JOIN ncm n ON i.co_ncm = n.co_ncm
INNER JOIN categorias_tecnologia c ON n.co_sh6 = c.co_sh6
GROUP BY
    i.co_ano,
    c.categoria
ORDER BY
    i.co_ano,
    c.categoria;
"""

df_importacoes = con.execute(query_importacoes).df()

fig, ax = plt.subplots(figsize=(13, 7))

for categoria, dados in df_importacoes.groupby("categoria"):
    linha, = ax.plot(
        dados["co_ano"],
        dados["importacoes_usd_bilhoes"],
        linewidth=2.5,
        label=NOMES_CATEGORIAS[categoria]
    )

    ultimo = dados.iloc[-1]

    ax.scatter(
        ultimo["co_ano"],
        ultimo["importacoes_usd_bilhoes"],
        color=linha.get_color(),
        s=45,
        zorder=3
    )

    valor = f'{ultimo["importacoes_usd_bilhoes"]:.2f}'.replace(".", ",")

    ax.text(
        ultimo["co_ano"] + 0.2,
        ultimo["importacoes_usd_bilhoes"],
        f'{NOMES_CATEGORIAS[categoria]} · US$ {valor} bi',
        color=linha.get_color(),
        va="center",
        fontsize=9.5
    )

ax.set_title(
    "Importações brasileiras de bens TIC por categoria",
    fontsize=16,
    pad=15
)
ax.set_xlabel("Ano")
ax.set_ylabel("US$ bilhões")
ax.set_xticks(range(2010, 2026, 2))
ax.set_xlim(2009.5, 2029)
ax.grid(axis="y", alpha=0.2)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

fig.text(
    0.01,
    0.01,
    "Fonte: Comex Stat/MDIC. Classificação de bens TIC baseada na UNCTAD.",
    fontsize=9
)

fig.tight_layout(rect=[0, 0.04, 1, 1])

fig.savefig(
    PASTA_GRAFICOS / "01_importacoes_por_categoria.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close(fig)

# ============================================================
# 2. EVOLUÇÃO DO SALDO COMERCIAL POR CATEGORIA
# ============================================================

query_saldo = """
WITH imp AS (
    SELECT
        i.co_ano,
        c.categoria,
        SUM(i.vl_fob) AS importacoes
    FROM importacoes i
    INNER JOIN ncm n ON i.co_ncm = n.co_ncm
    INNER JOIN categorias_tecnologia c ON n.co_sh6 = c.co_sh6
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
    GROUP BY
        e.co_ano,
        c.categoria
)
SELECT
    i.co_ano,
    i.categoria,
    (e.exportacoes - i.importacoes) / 1000000000.0 AS saldo_usd_bilhoes
FROM imp i
INNER JOIN exp e ON i.co_ano = e.co_ano AND i.categoria = e.categoria
ORDER BY
    i.co_ano,
    i.categoria;
"""

df_saldo = con.execute(query_saldo).df()

fig, ax = plt.subplots(figsize=(13, 7))

for categoria, dados in df_saldo.groupby("categoria"):
    linha, = ax.plot(
        dados["co_ano"],
        dados["saldo_usd_bilhoes"],
        linewidth=2.5,
        label=NOMES_CATEGORIAS[categoria]
    )

    ultimo = dados.iloc[-1]

    ax.scatter(
        ultimo["co_ano"],
        ultimo["saldo_usd_bilhoes"],
        color=linha.get_color(),
        s=45,
        zorder=3
    )

    valor = f'{ultimo["saldo_usd_bilhoes"]:.2f}'.replace(".", ",")

    ax.text(
        ultimo["co_ano"] + 0.2,
        ultimo["saldo_usd_bilhoes"],
        f'{NOMES_CATEGORIAS[categoria]} · US$ {valor} bi',
        color=linha.get_color(),
        va="center",
        fontsize=9.5
    )

ax.axhline(
    0,
    linewidth=1,
    color="black",
    alpha=0.5
)

ax.set_title(
    "Saldo comercial brasileiro de bens TIC por categoria",
    fontsize=16,
    pad=15
)
ax.set_xlabel("Ano")
ax.set_ylabel("US$ bilhões")
ax.set_xticks(range(2010, 2026, 2))
ax.set_xlim(2009.5, 2029)
ax.grid(axis="y", alpha=0.2)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

fig.text(
    0.01,
    0.01,
    "Saldo = exportações − importações. Fonte: Comex Stat/MDIC. Classificação de bens TIC baseada na UNCTAD.",
    fontsize=9
)

fig.tight_layout(rect=[0, 0.04, 1, 1])

fig.savefig(
    PASTA_GRAFICOS / "02_saldo_por_categoria.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close(fig)

# ============================================================
# 3. PRINCIPAIS PAÍSES FORNECEDORES EM 2025
# ============================================================

query_fornecedores = """
SELECT
    p.no_pais,
    SUM(i.vl_fob) / 1000000000.0 AS importacoes_usd_bilhoes
FROM importacoes i
INNER JOIN ncm n ON i.co_ncm = n.co_ncm
INNER JOIN categorias_tecnologia c ON n.co_sh6 = c.co_sh6
INNER JOIN paises p ON i.co_pais = p.co_pais
WHERE i.co_ano = 2025
GROUP BY
    p.no_pais
ORDER BY
    importacoes_usd_bilhoes DESC
LIMIT 10;
"""

df_fornecedores = con.execute(query_fornecedores).df()

df_fornecedores = df_fornecedores.sort_values(
    "importacoes_usd_bilhoes"
)

fig, ax = plt.subplots(figsize=(11, 7))

barras = ax.barh(
    df_fornecedores["no_pais"],
    df_fornecedores["importacoes_usd_bilhoes"]
)

ax.bar_label(
    barras,
    labels=[
        f'US$ {valor:.2f} bi'.replace(".", ",")
        for valor in df_fornecedores["importacoes_usd_bilhoes"]
    ],
    padding=5,
    fontsize=9
)

ax.set_title(
    "Principais fornecedores de bens TIC ao Brasil — 2025",
    fontsize=16,
    pad=15
)
ax.set_xlabel("Importações (US$ bilhões)")
ax.set_ylabel("")
ax.set_xlim(
    0,
    df_fornecedores["importacoes_usd_bilhoes"].max() * 1.18
)
ax.grid(axis="x", alpha=0.15)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_visible(False)

fig.text(
    0.01,
    0.01,
    "Fonte: Comex Stat/MDIC. Classificação de bens TIC baseada na UNCTAD.",
    fontsize=9
)

fig.tight_layout(rect=[0, 0.04, 1, 1])

fig.savefig(
    PASTA_GRAFICOS / "03_principais_fornecedores.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close(fig)

# ============================================================
# 4. PRODUTOS COM MAIOR DÉFICIT EM 2025
# ============================================================

query_produtos = """
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
    n.co_ncm,
    n.no_ncm_por AS produto,
    (COALESCE(e.exportacoes, 0) - COALESCE(i.importacoes, 0))
        / 1000000000.0 AS saldo_usd_bilhoes
FROM ncm n
INNER JOIN categorias_tecnologia c ON n.co_sh6 = c.co_sh6
LEFT JOIN imp i ON n.co_ncm = i.co_ncm
LEFT JOIN exp e ON n.co_ncm = e.co_ncm
WHERE i.co_ncm IS NOT NULL OR e.co_ncm IS NOT NULL
ORDER BY
    saldo_usd_bilhoes
LIMIT 10;
"""

df_produtos = con.execute(query_produtos).df()

NOMES_PRODUTOS = {
    "85423120": "Processadores e controladores",
    "85423939": "Outros circuitos integrados monolíticos",
    "85423190": "Outros circuitos integrados",
    "84714900": "Sistemas de processamento de dados",
    "85423210": "Memórias não montadas",
    "85423229": "Outras memórias digitais montadas",
    "84733090": "Partes e acessórios de computadores",
    "85176259": "Equipamentos terminais ou repetidores",
    "84715040": "Unidades de processamento digital",
    "85299020": "Partes para aparelhos receptores"
}

df_produtos["produto_grafico"] = df_produtos.apply(
    lambda linha: NOMES_PRODUTOS.get(
        linha["co_ncm"],
        linha["produto"]
    ),
    axis=1
)

df_produtos["deficit_usd_bilhoes"] = (
    -df_produtos["saldo_usd_bilhoes"]
)

df_produtos = df_produtos.sort_values(
    "deficit_usd_bilhoes"
)

fig, ax = plt.subplots(figsize=(11, 7))

barras = ax.barh(
    df_produtos["produto_grafico"],
    df_produtos["deficit_usd_bilhoes"]
)

ax.bar_label(
    barras,
    labels=[
        f'US$ {valor:.2f} bi'.replace(".", ",")
        for valor in df_produtos["deficit_usd_bilhoes"]
    ],
    padding=5,
    fontsize=9
)

ax.set_title(
    "Produtos TIC com maior déficit comercial — 2025",
    fontsize=16,
    pad=15
)
ax.set_xlabel("Déficit comercial (US$ bilhões)")
ax.set_ylabel("")
ax.set_xlim(
    0,
    df_produtos["deficit_usd_bilhoes"].max() * 1.18
)
ax.grid(axis="x", alpha=0.15)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_visible(False)

fig.text(
    0.01,
    0.01,
    "Saldo = exportações − importações. Valores apresentados como magnitude do déficit. Fonte: Comex Stat/MDIC.",
    fontsize=9
)

fig.tight_layout(rect=[0, 0.04, 1, 1])

fig.savefig(
    PASTA_GRAFICOS / "04_produtos_maior_deficit.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close(fig)

con.close()

print("Gráficos atualizados com sucesso:")
print(PASTA_GRAFICOS / "01_importacoes_por_categoria.png")
print(PASTA_GRAFICOS / "02_saldo_por_categoria.png")
print(PASTA_GRAFICOS / "03_principais_fornecedores.png")
print(PASTA_GRAFICOS / "04_produtos_maior_deficit.png")