from pathlib import Path

import pandas as pd

# ============================================================
# CAMINHOS
# ============================================================

PASTA_PROJETO = Path(__file__).resolve().parent.parent
PASTA_DADOS = PASTA_PROJETO / "dados" / "brutos"

ARQUIVO_IMPORTACOES = PASTA_DADOS / "IMP_2025.csv"
ARQUIVO_EXPORTACOES = PASTA_DADOS / "EXP_2025.csv"
ARQUIVO_NCM = PASTA_DADOS / "NCM.csv"
ARQUIVO_PAISES = PASTA_DADOS / "PAIS.csv"

# ============================================================
# IMPORTAÇÕES
# ============================================================

df_importacoes = pd.read_csv(
    ARQUIVO_IMPORTACOES,
    sep=";",
    nrows=10_000
)

print("=== IMPORTAÇÕES 2025 ===")

print("\nDimensões da amostra:")
print(df_importacoes.shape)

print("\nColunas:")
print(df_importacoes.columns.tolist())

print("\nPrimeiras 5 linhas:")
print(df_importacoes.head())

print("\nTipos:")
print(df_importacoes.dtypes)

print("\nValores nulos:")
print(df_importacoes.isna().sum())

# ============================================================
# NCM
# ============================================================

df_ncm = pd.read_csv(
    ARQUIVO_NCM,
    sep=";",
    encoding="latin1"
)

print("\n=== TABELA NCM ===")

print("\nDimensões:")
print(df_ncm.shape)

print("\nColunas:")
print(df_ncm.columns.tolist())

print("\nPrimeiras 5 linhas:")
print(df_ncm.head())

print("\nTipos:")
print(df_ncm.dtypes)

# ============================================================
# PAÍSES
# ============================================================

df_paises = pd.read_csv(
    ARQUIVO_PAISES,
    sep=";",
    encoding="latin1"
)

print("\n=== TABELA DE PAÍSES ===")

print("\nDimensões:")
print(df_paises.shape)

print("\nColunas:")
print(df_paises.columns.tolist())

print("\nPrimeiras 5 linhas:")
print(df_paises.head())

print("\nTipos:")
print(df_paises.dtypes)