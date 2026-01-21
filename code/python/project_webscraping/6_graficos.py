
# PROJETO: Web Scraping de Dados – Visualização Gráfica
# OBJETIVO: Gerar gráficos analíticos da distribuição populacional dos municípios brasileiros
# AUTOR: RODRIGO GARCIA BRUNINI
# DATA: 20/01/2026
# VERSÃO: 1.0

# Metodologia:
"""
Este script gera visualizações gráficas para análise da distribuição populacional brasileira.

ETAPAS DO PROCESSO:
1. LEITURA: Carrega o arquivo consolidado de municípios com população
2. LIMPEZA: Padroniza formato numérico e remove registros sem dados
3. PREPARAÇÃO: Cria identificadores compostos (Município + UF)
4. AGREGAÇÃO: Agrupa dados por Estado, Região e Município
5. VISUALIZAÇÃO: Gera 4 gráficos diferentes para análise
6. EXPORTAÇÃO: Salva todas as imagens em formato PNG

GRÁFICOS GERADOS:
1. Barras - População por Estado (UF): mostra total populacional de cada estado
2. Pizza - População por Região: exibe distribuição percentual entre as 5 regiões
3. Colunas - Top 10 Maiores Municípios: destaca as cidades mais populosas
4. Colunas - Top 10 Menores Municípios: identifica as cidades menos populosas

GLOSSÁRIO:
- groupby: agrupa dados por categoria (ex: agrupar municípios por estado)
- sum(): soma valores de uma coluna
- sort_values: ordena dados de forma crescente ou decrescente
- ascending=False: ordem decrescente (maior para menor)
- head(10): seleciona apenas os 10 primeiros registros
- autopct: formato de exibição de percentuais no gráfico de pizza
- tight_layout: ajusta espaçamento automático para evitar sobreposição
- ha="right": alinha texto à direita (horizontal alignment)

DEPENDÊNCIAS:
pip install pandas matplotlib

RESULTADO:
Gráficos salvos em: C:/Users/<seu_usuario>/Desktop/projetos/graficos/
- populacao_por_estado.png
- populacao_por_regiao.png
- top10_maiores_municipios.png
- top10_menores_municipios.png
"""

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Caminhos
OUTDIR = Path.home() / "Desktop" / "ebac" / "EBAC_PYTHON_WEBSCRAPING" / "data" / "ready"
input_path = OUTDIR / "pop_mun_final.csv"
output_dir = Path.home() / "Desktop" / "ebac" / "EBAC_PYTHON_WEBSCRAPING" / "graficos"
Path(output_dir).mkdir(parents=True, exist_ok=True)

# Leitura dos dados
df = pd.read_csv(input_path, dtype=str)
df.columns = [c.strip() for c in df.columns]

# Conversão da população para formato numérico
df["POPULAÇÃO ESTIMADA"] = (
    df["POPULAÇÃO ESTIMADA"]
    .str.replace(".", "", regex=False)
    .str.replace(",", ".", regex=False)
)
df["POPULAÇÃO ESTIMADA"] = pd.to_numeric(df["POPULAÇÃO ESTIMADA"], errors="coerce")

# Remove registros sem população
df = df.dropna(subset=["POPULAÇÃO ESTIMADA"])

# Cria identificador completo: Município + UF
df["MUNICIPIO_UF"] = df["nome"] + " - " + df["uf_sigla"]

# ================================
# 1) Gráfico de barras - População por Estado
# ================================
pop_uf = (
    df.groupby("uf_sigla")["POPULAÇÃO ESTIMADA"]
    .sum()
    .sort_values(ascending=False)
)

plt.figure(figsize=(12,6))
pop_uf.plot(kind="bar")
plt.title("População Estimada por Estado (UF)")
plt.xlabel("Estado (UF)")
plt.ylabel("População Estimada")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(f"{output_dir}\\populacao_por_estado.png")
plt.close()

# ================================
# 2) Gráfico de pizza - População por Região
# ================================
pop_regiao = (
    df.groupby("regiao")["POPULAÇÃO ESTIMADA"]
    .sum()
)

plt.figure(figsize=(8,8))
pop_regiao.plot(kind="pie", autopct="%1.1f%%")
plt.title("Distribuição da População por Região")
plt.ylabel("")
plt.tight_layout()
plt.savefig(f"{output_dir}\\populacao_por_regiao.png")
plt.close()

# ================================
# 3) Gráfico de colunas - Top 10 municípios mais populosos
# ================================
top10_maiores = (
    df.groupby("MUNICIPIO_UF")["POPULAÇÃO ESTIMADA"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

plt.figure(figsize=(12,6))
top10_maiores.plot(kind="bar")
plt.title("Top 10 Municípios Mais Populosos do Brasil")
plt.xlabel("Município - UF")
plt.ylabel("População Estimada")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig(f"{output_dir}\\top10_maiores_municipios.png")
plt.close()

# ================================
# 4) Gráfico de colunas - Top 10 municípios menos populosos
# ================================
top10_menores = (
    df.groupby("MUNICIPIO_UF")["POPULAÇÃO ESTIMADA"]
    .sum()
    .sort_values(ascending=True)
    .head(10)
)

plt.figure(figsize=(12,6))
top10_menores.plot(kind="bar")
plt.title("Top 10 Municípios Menos Populosos do Brasil")
plt.xlabel("Município - UF")
plt.ylabel("População Estimada")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig(f"{output_dir}\\top10_menores_municipios.png")
plt.close()

print("Gráficos gerados com sucesso em:")
print(output_dir)

# Fim do script
