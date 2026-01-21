
# PROJETO: Web Scraping de Dados – Integração Final
# OBJETIVO: Unificar a base de municípios do IBGE com a base de população, criando um arquivo final padronizado.
# AUTOR: RODRIGO GARCIA BRUNINI
# DATA: 20/01/2026
# VERSÃO: 1.0

# Metodologia:
"""
Este script integra duas bases de dados diferentes do IBGE:

1. Base de municípios (municipios.csv)
2. Base de população corrigida (pop_corrigida.csv)

ETAPAS DO PROCESSO:
1. LEITURA: Carrega os dois arquivos CSV (municípios e população)
2. PADRONIZAÇÃO: Corrige nomes de colunas e garante que id_ibge esteja no formato string
3. FILTRO: Seleciona apenas as colunas necessárias da base populacional
4. JUNÇÃO: Realiza merge entre as bases usando id_ibge como chave
5. EXPORTAÇÃO: Gera o arquivo final com todos os municípios + população estimada

RESULTADO:
- Arquivo final salvo em: C:/Users/<seu_usuario>/Desktop/projetos/data/ready/pop_mun_final.csv
- O arquivo contém:
    id_ibge, nome, uf_sigla, uf_nome, regiao, POPULAÇÃO ESTIMADA

GLOSSÁRIO:
- merge: técnica para unir duas tabelas com base em uma coluna em comum
- left join: mantém todos os municípios, mesmo se algum não tiver população associada
- id_ibge: identificador oficial do município (7 dígitos)
"""

import pandas as pd
from pathlib import Path

# Caminhos
INPUTDIR = Path.home() / "Desktop" / "ebac" / "EBAC_PYTHON_WEBSCRAPING" / "data" / "raw"
OUTDIR = Path.home() / "Desktop" / "ebac" / "EBAC_PYTHON_WEBSCRAPING" / "data" / "ready"

municipios_path = INPUTDIR / "municipios.csv"
pop_path = INPUTDIR / "pop_corrigida.csv"
output_path = OUTDIR / "pop_mun_final.csv"

# Leitura dos arquivos
df_mun = pd.read_csv(municipios_path, dtype=str)
df_pop = pd.read_csv(pop_path, dtype=str)

# Padroniza nome das colunas
df_mun.columns = [c.strip() for c in df_mun.columns]
df_pop.columns = [c.strip() for c in df_pop.columns]

# Garante que id_ibge é string
df_mun["id_ibge"] = df_mun["id_ibge"].astype(str)
df_pop["id_ibge"] = df_pop["id_ibge"].astype(str)

# Mantém apenas colunas necessárias da população
df_pop = df_pop[["id_ibge", "POPULAÇÃO ESTIMADA"]]

# Faz a junção das tabelas pelo id_ibge
df_final = df_mun.merge(df_pop, on="id_ibge", how="left")

# Cria pasta de destino se não existir
Path(output_path).parent.mkdir(parents=True, exist_ok=True)

# Salva resultado final
df_final.to_csv(output_path, index=False, encoding="utf-8")

print("Arquivo gerado com sucesso:")
print(output_path)

# Fim do script #