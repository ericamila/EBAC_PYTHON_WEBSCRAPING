# PROJETO: Web Scraping de Dados – Mapeamento Geoespacial
# OBJETIVO: Gerar mapa temático da distribuição populacional dos municípios brasileiros com divisas estaduais
# AUTOR: RODRIGO GARCIA BRUNINI
# DATA: 20/01/2026
# VERSÃO: 1.0

# Metodologia:
"""
Este script cria um mapa coroplético (colorido por valores) da população municipal brasileira.

ETAPAS DO PROCESSO:
1. LEITURA: Carrega dados populacionais (CSV) e malha geográfica municipal (Shapefile)
2. PADRONIZAÇÃO: Ajusta códigos IBGE e formatos numéricos para garantir compatibilidade
3. JUNÇÃO ESPACIAL: Associa dados populacionais às geometrias dos municípios
4. AGREGAÇÃO GEOGRÁFICA: Cria divisas estaduais através de dissolução de polígonos municipais
5. VISUALIZAÇÃO: Gera mapa temático com escala logarítmica de cores
6. EXPORTAÇÃO: Salva imagem em alta resolução (300 DPI)

CARACTERÍSTICAS DO MAPA:
- Escala de cores: RdYlBu_r (vermelho = maior população, azul = menor)
- Escala logarítmica: compensa diferenças extremas entre municípios pequenos e grandes
- Divisas estaduais: linhas pretas destacadas para facilitar identificação geográfica
- Bordas municipais: linhas cinzas finas para delimitar cada município
- Resolução: 300 DPI (qualidade para impressão)

GLOSSÁRIO:
- Shapefile (.shp): formato padrão para dados geográficos vetoriais
- GeoDataFrame: tabela com geometrias espaciais (polígonos, linhas, pontos)
- dissolve: operação que une polígonos adjacentes com mesma característica
- LogNorm: normalização logarítmica para lidar com valores muito discrepantes
- cmap: mapa de cores (color map)
- DPI: dots per inch, define qualidade da imagem
- boundary: contorno/borda de um polígono
- edgecolor: cor das bordas dos polígonos

DEPENDÊNCIAS:
pip install pandas geopandas matplotlib

FONTE DA MALHA GEOGRÁFICA:
IBGE - Malha Municipal 2024
Arquivo: RR_Municipios_2024.shp

RESULTADO:
Mapa salvo em: C:/Users/<seu_usuario>/Desktop/projetos/graficos/mapa_populacao_municipios_com_divisas_roraima.png
"""

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from pathlib import Path
from matplotlib.colors import LogNorm

# ============================
# Caminhos
# ============================
OUTDIR = Path.home() / "Desktop" / "ebac" / "EBAC_PYTHON_WEBSCRAPING" / "data"
data_path = OUTDIR / "ready" / "pop_mun_final.csv"
map_mun_path = OUTDIR / "dados_shapefile" / "RR_Municipios_2024" / "RR_Municipios_2024.shp"
output_dir = Path.home() / "Desktop" / "ebac" / "EBAC_PYTHON_WEBSCRAPING" / "graficos"
output_map = output_dir / "mapa_populacao_municipios_com_divisas_estaduais_roraima.png"
Path(output_dir).mkdir(parents=True, exist_ok=True)

# ============================
# Base populacional
# ============================
df = pd.read_csv(data_path, dtype=str)
df.columns = [c.strip().lower() for c in df.columns]

# Padroniza código IBGE para 7 dígitos
df["id_ibge"] = df["id_ibge"].str.replace(".0", "", regex=False).str.zfill(7)

# Converte população para formato numérico
df["populacao_estimada"] = (
    df["população estimada"]
    .str.replace(".", "", regex=False)
    .str.replace(",", ".", regex=False)
)
df["populacao_estimada"] = pd.to_numeric(df["populacao_estimada"], errors="coerce")

# Remove registros sem dados válidos
df = df.dropna(subset=["id_ibge", "populacao_estimada"])

# ============================
# Malha municipal
# ============================
mun = gpd.read_file(map_mun_path)
mun.columns = [c.lower() for c in mun.columns]

# Identifica colunas relevantes automaticamente
col_ibge = [c for c in mun.columns if "cd_mun" in c or "cod" in c][0]
col_mun  = [c for c in mun.columns if "cd_mun" in c or "cod" in c][0]  # Usado para dissolve

# Padroniza código IBGE no shapefile
mun["id_ibge"] = mun[col_ibge].astype(str).str.replace(".0", "", regex=False).str.zfill(7)

# Faz junção entre dados populacionais e geometrias
geo = mun.merge(df[["id_ibge", "populacao_estimada"]], on="id_ibge", how="left")
geo = geo[geo["populacao_estimada"].notna()]

# ============================
# Criar divisas estaduais (dissolve)
# ============================
# Agrupa para formar contornos municipais
municipios = geo.dissolve(by=col_mun)

# ============================
# Geração do mapa
# ============================
fig, ax = plt.subplots(figsize=(14, 14))

# Define limites da escala de cores
vmin = geo["populacao_estimada"].min()
vmax = geo["populacao_estimada"].max()

# Plota municípios com cores baseadas na população
geo.plot(
    column="populacao_estimada",
    cmap="RdYlBu_r",
    linewidth=0.05,
    edgecolor="gray",
    norm=LogNorm(vmin=vmin, vmax=vmax),
    legend=True,
    legend_kwds={
        "label": "População Estimada por Município (escala logarítmica)",
        "shrink": 0.6
    },
    ax=ax
)

# Adiciona divisas estaduais com linha grossa
municipios.boundary.plot(
    ax=ax,
    linewidth=1.8,
    edgecolor="black"
)

ax.set_title("Mapa de Roraima: Densidade Populacional por Municípios", fontsize=16)
ax.axis("off")
plt.tight_layout()
plt.savefig(output_map, dpi=300)
plt.close()

print("\nMapa gerado com sucesso em:")
print(output_map)

# Fim do script
