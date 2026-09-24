from pathlib import Path
import duckdb


# CAMINHOS
PASTA_PROJETO = Path(__file__).resolve().parent.parent
PASTA_DADOS = PASTA_PROJETO / "dados" / "brutos"
ARQUIVOS_IMPORTACOES = str(PASTA_DADOS / "IMP_*.csv")
ARQUIVOS_EXPORTACOES = str(PASTA_DADOS / "EXP_*.csv")
ARQUIVO_NCM = PASTA_DADOS / "NCM.csv"
ARQUIVO_PAISES = PASTA_DADOS / "PAIS.csv"
ARQUIVO_BANCO = PASTA_PROJETO / "dados" / "soberania_digital.duckdb"


# CONEXÃO
conexao = duckdb.connect(ARQUIVO_BANCO)

# IMPORTAÇÕES
print("Criando tabela de importações...")

conexao.execute(f"""
    CREATE OR REPLACE TABLE importacoes AS
    SELECT
        CO_ANO::INTEGER AS co_ano,
        CO_MES::INTEGER AS co_mes,
        CO_NCM::VARCHAR AS co_ncm,
        CO_UNID::VARCHAR AS co_unid,
        CO_PAIS::VARCHAR AS co_pais,
        SG_UF_NCM::VARCHAR AS sg_uf_ncm,
        CO_VIA::VARCHAR AS co_via,
        CO_URF::VARCHAR AS co_urf,
        QT_ESTAT::BIGINT AS qt_estat,
        KG_LIQUIDO::BIGINT AS kg_liquido,
        VL_FOB::BIGINT AS vl_fob,
        VL_FRETE::BIGINT AS vl_frete,
        VL_SEGURO::BIGINT AS vl_seguro
    FROM read_csv(
        '{ARQUIVOS_IMPORTACOES}',
        delim = ';',
        header = true,
        union_by_name = true,
        all_varchar = true
    )
    WHERE CO_ANO::INTEGER BETWEEN 2010 AND 2025
""")

# EXPORTAÇÕES
print("Criando tabela de exportações...")

conexao.execute(f"""
    CREATE OR REPLACE TABLE exportacoes AS
    SELECT
        CO_ANO::INTEGER AS co_ano,
        CO_MES::INTEGER AS co_mes,
        CO_NCM::VARCHAR AS co_ncm,
        CO_UNID::VARCHAR AS co_unid,
        CO_PAIS::VARCHAR AS co_pais,
        SG_UF_NCM::VARCHAR AS sg_uf_ncm,
        CO_VIA::VARCHAR AS co_via,
        CO_URF::VARCHAR AS co_urf,
        QT_ESTAT::BIGINT AS qt_estat,
        KG_LIQUIDO::BIGINT AS kg_liquido,
        VL_FOB::BIGINT AS vl_fob
    FROM read_csv(
        '{ARQUIVOS_EXPORTACOES}',
        delim = ';',
        header = true,
        union_by_name = true,
        all_varchar = true
    )
    WHERE CO_ANO::INTEGER BETWEEN 2010 AND 2025
""")

# NCM
print("Criando tabela NCM...")

conexao.execute(f"""
    CREATE OR REPLACE TABLE ncm AS
    SELECT
        CO_NCM::VARCHAR AS co_ncm,
        CO_UNID::VARCHAR AS co_unid,
        CO_SH6::VARCHAR AS co_sh6,
        CO_PPE::VARCHAR AS co_ppe,
        CO_PPI::VARCHAR AS co_ppi,
        CO_FAT_AGREG::VARCHAR AS co_fat_agreg,
        CO_CUCI_ITEM::VARCHAR AS co_cuci_item,
        CO_CGCE_N3::VARCHAR AS co_cgce_n3,
        CO_SIIT::VARCHAR AS co_siit,
        CO_ISIC_CLASSE::VARCHAR AS co_isic_classe,
        CO_EXP_SUBSET::VARCHAR AS co_exp_subset,
        NO_NCM_POR::VARCHAR AS no_ncm_por,
        NO_NCM_ESP::VARCHAR AS no_ncm_esp,
        NO_NCM_ING::VARCHAR AS no_ncm_ing
    FROM read_csv(
        '{ARQUIVO_NCM}',
        delim = ';',
        header = true,
        encoding = 'latin-1',
        strict_mode = false,
        all_varchar = true
    )
""")

# PAÍSES
print("Criando tabela de países...")

conexao.execute(f"""
    CREATE OR REPLACE TABLE paises AS
    SELECT
        CO_PAIS::VARCHAR AS co_pais,
        CO_PAIS_ISON3::VARCHAR AS co_pais_ison3,
        CO_PAIS_ISOA3::VARCHAR AS co_pais_isoa3,
        NO_PAIS::VARCHAR AS no_pais,
        NO_PAIS_ING::VARCHAR AS no_pais_ing,
        NO_PAIS_ESP::VARCHAR AS no_pais_esp
    FROM read_csv(
        '{ARQUIVO_PAISES}',
        delim = ';',
        header = true,
        encoding = 'latin-1',
        strict_mode = false,
        all_varchar = true
    )
""")

# CATEGORIAS DE TECNOLOGIA
print("Criando tabela de categorias de tecnologia...")

conexao.execute("""
    CREATE OR REPLACE TABLE categorias_tecnologia (
        co_sh6 VARCHAR,
        categoria_ict VARCHAR,
        categoria VARCHAR
    )
""")

categorias_tecnologia = {
    "ICT01": {
        "categoria": "computadores_perifericos",
        "codigos": [
            "844331",
            "844332",
            "847050",
            "847130",
            "847141",
            "847149",
            "847150",
            "847160",
            "847170",
            "847180",
            "847190",
            "847290",
            "847330",
            "847340",
            "847350",
            "852842",
            "852852",
        ],
    },
    "ICT02": {
        "categoria": "equipamentos_comunicacao",
        "codigos": [
            "851711",
            "851712",
            "851718",
            "851761",
            "851762",
            "851769",
            "851770",
            "852550",
            "852560",
            "853110",
        ],
    },
    "ICT03": {
        "categoria": "eletronicos_consumo",
        "codigos": [
            "851810",
            "851821",
            "851822",
            "851829",
            "851830",
            "851840",
            "851850",
            "851890",
            "851920",
            "851930",
            "851950",
            "851981",
            "851989",
            "852110",
            "852190",
            "852210",
            "852290",
            "852580",
            "852712",
            "852713",
            "852719",
            "852721",
            "852729",
            "852791",
            "852792",
            "852799",
            "852849",
            "852859",
            "852862",
            "852869",
            "852871",
            "852872",
            "852873",
            "950450",
        ],
    },
    "ICT04": {
        "categoria": "componentes_eletronicos",
        "codigos": [
            "852321",
            "852352",
            "853400",
            "854011",
            "854012",
            "854020",
            "854040",
            "854060",
            "854071",
            "854079",
            "854081",
            "854089",
            "854091",
            "854099",
            "854110",
            "854121",
            "854129",
            "854130",
            "854140",
            "854150",
            "854160",
            "854190",
            "854231",
            "854232",
            "854233",
            "854239",
            "854290",
        ],
    },
    "ICT05": {
        "categoria": "outros_bens_ict",
        "codigos": [
            "852351",
            "852359",
            "852380",
            "852910",
            "852990",
            "901320",
        ],
    },
}

registros = []

for categoria_ict, dados in categorias_tecnologia.items():
    for co_sh6 in dados["codigos"]:
        registros.append(
            (
                co_sh6,
                categoria_ict,
                dados["categoria"],
            )
        )

conexao.executemany(
    """
    INSERT INTO categorias_tecnologia (
        co_sh6,
        categoria_ict,
        categoria
    )
    VALUES (?, ?, ?)
    """,
    registros,
)

# VALIDAÇÃO — IMPORTAÇÕES POR ANO
print("\n=== IMPORTAÇÕES POR ANO ===")

importacoes_por_ano = conexao.execute("""
    SELECT
        co_ano,
        COUNT(*) AS registros
    FROM importacoes
    GROUP BY co_ano
    ORDER BY co_ano
""").fetchdf()

print(importacoes_por_ano.to_string(index=False))

# VALIDAÇÃO — EXPORTAÇÕES POR ANO
print("\n=== EXPORTAÇÕES POR ANO ===")

exportacoes_por_ano = conexao.execute("""
    SELECT
        co_ano,
        COUNT(*) AS registros
    FROM exportacoes
    GROUP BY co_ano
    ORDER BY co_ano
""").fetchdf()

print(exportacoes_por_ano.to_string(index=False))

# VALIDAÇÃO — PERÍODO
print("\n=== PERÍODO DISPONÍVEL ===")

periodo = conexao.execute("""
    SELECT
        MIN(co_ano) AS primeiro_ano,
        MAX(co_ano) AS ultimo_ano,
        COUNT(DISTINCT co_ano) AS quantidade_anos
    FROM importacoes
""").fetchdf()

print(periodo.to_string(index=False))


# VALIDAÇÃO — TOTAL DE REGISTROS
print("\n=== QUANTIDADE TOTAL DE REGISTROS ===")

totais = conexao.execute("""
    SELECT
        'importacoes' AS tabela,
        COUNT(*) AS registros
    FROM importacoes

    UNION ALL

    SELECT
        'exportacoes',
        COUNT(*)
    FROM exportacoes

    UNION ALL

    SELECT
        'ncm',
        COUNT(*)
    FROM ncm

    UNION ALL

    SELECT
        'paises',
        COUNT(*)
    FROM paises

    UNION ALL

    SELECT
        'categorias_tecnologia',
        COUNT(*)
    FROM categorias_tecnologia
""").fetchdf()

print(totais.to_string(index=False))

# VALIDAÇÃO — TIPOS
print("\n=== TIPOS — IMPORTAÇÕES ===")

tipos_importacoes = conexao.execute("""
    DESCRIBE importacoes
""").fetchdf()

print(
    tipos_importacoes[
        ["column_name", "column_type", "null"]
    ].to_string(index=False)
)

print("\n=== TIPOS — NCM ===")

tipos_ncm = conexao.execute("""
    DESCRIBE ncm
""").fetchdf()

print(
    tipos_ncm[
        ["column_name", "column_type", "null"]
    ].to_string(index=False)
)

# VALIDAÇÃO — CATEGORIAS DE TECNOLOGIA
print("\n=== CATEGORIAS DE TECNOLOGIA ===")

categorias = conexao.execute("""
    SELECT
        categoria_ict,
        categoria,
        COUNT(*) AS codigos_sh6
    FROM categorias_tecnologia
    GROUP BY
        categoria_ict,
        categoria
    ORDER BY
        categoria_ict
""").fetchdf()

print(categorias.to_string(index=False))

# VALIDAÇÃO — COBERTURA DE BENS TIC
print("\n=== BENS TIC ENCONTRADOS NAS IMPORTAÇÕES ===")

cobertura_importacoes = conexao.execute("""
    SELECT
        i.co_ano,
        COUNT(DISTINCT c.co_sh6) AS codigos_ict_encontrados,
        ROUND(
            SUM(
                CASE
                    WHEN c.co_sh6 IS NOT NULL THEN i.vl_fob
                    ELSE 0
                END
            ) / 1000000000.0,
            2
        ) AS valor_ict_usd_bilhoes
    FROM importacoes i
    LEFT JOIN ncm n ON i.co_ncm = n.co_ncm
    LEFT JOIN categorias_tecnologia c ON n.co_sh6 = c.co_sh6
    GROUP BY
        i.co_ano
    ORDER BY
        i.co_ano
""").fetchdf()

print(cobertura_importacoes.to_string(index=False))

print("\n=== BENS TIC ENCONTRADOS NAS EXPORTAÇÕES ===")

cobertura_exportacoes = conexao.execute("""
    SELECT
        e.co_ano,
        COUNT(DISTINCT c.co_sh6) AS codigos_ict_encontrados,
        ROUND(
            SUM(
                CASE
                    WHEN c.co_sh6 IS NOT NULL THEN e.vl_fob
                    ELSE 0
                END
            ) / 1000000000.0,
            2
        ) AS valor_ict_usd_bilhoes
    FROM exportacoes e
    LEFT JOIN ncm n ON e.co_ncm = n.co_ncm
    LEFT JOIN categorias_tecnologia c ON n.co_sh6 = c.co_sh6
    GROUP BY
        e.co_ano
    ORDER BY
        e.co_ano
""").fetchdf()

print(cobertura_exportacoes.to_string(index=False))

conexao.close()

print("\nBanco criado com sucesso.")
print(ARQUIVO_BANCO)