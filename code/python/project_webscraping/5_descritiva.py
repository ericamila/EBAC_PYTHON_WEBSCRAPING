
# PROJETO: Web Scraping de Dados – Análise Estatística
# OBJETIVO: Gerar relatório estatístico descritivo da população dos municípios brasileiros
# AUTOR: RODRIGO GARCIA BRUNINI
# DATA: 20/01/2026
# VERSÃO: 1.0

# Metodologia:
"""
Este script realiza análise estatística descritiva dos dados populacionais dos municípios brasileiros.

ETAPAS DO PROCESSO:
1. LEITURA: Carrega o arquivo consolidado de municípios com população
2. LIMPEZA: Padroniza formato numérico da população (remove pontos/vírgulas)
3. CONVERSÃO: Transforma dados de texto para valores numéricos
4. ANÁLISE DESCRITIVA: Calcula média, mediana, desvio padrão, mínimo e máximo
5. DETECÇÃO DE OUTLIERS: Identifica municípios com população atípica usando método IQR
6. CONSOLIDAÇÃO: Gera relatório estruturado com todas as métricas
7. EXPORTAÇÃO: Salva relatório em CSV e exibe resumo no terminal

MÉTRICAS CALCULADAS:
- Total de Municípios: quantidade de registros válidos
- População Média: soma total dividida pelo número de municípios
- População Mediana: valor central quando ordenados
- Desvio Padrão: medida de dispersão dos dados
- Mínimo/Máximo: menor e maior população registrada
- Quartis (Q1, Q3): divisões em 25% e 75% dos dados
- Valores Ausentes: municípios sem informação populacional
- Outliers: municípios com população muito diferente do padrão

GLOSSÁRIO:
- Outliers: valores extremos que fogem do padrão esperado
- IQR (Intervalo Interquartil): diferença entre Q3 e Q1, usado para detectar outliers
- Quartil: divisão dos dados em 4 partes iguais
- Desvio Padrão: indica o quanto os valores variam em relação à média
- Mediana: valor do meio, menos sensível a valores extremos que a média
- coerce: força conversão para número, transformando erros em NaN (valor ausente)

RESULTADO:
Arquivo salvo em: C:/Users/<seu_usuario>/Desktop/projetos/data/ready/relatorio_estatistico_pop.csv
"""

import pandas as pd
from pathlib import Path

# Caminho do arquivo
OUTDIR = Path.home() / "Desktop" / "ebac" / "EBAC_PYTHON_WEBSCRAPING" / "data" / "ready"

input_path = OUTDIR /"pop_mun_final.csv"
output_path = OUTDIR / "relatorio_estatistico_pop.csv"

# Leitura dos dados
df = pd.read_csv(input_path, dtype=str)

# Padroniza nomes de colunas
df.columns = [c.strip() for c in df.columns]

# Converte população para formato numérico
# Remove pontos de milhar e substitui vírgula decimal por ponto
df["POPULAÇÃO ESTIMADA"] = (
    df["POPULAÇÃO ESTIMADA"]
    .str.replace(".", "", regex=False)
    .str.replace(",", ".", regex=False)
)
df["POPULAÇÃO ESTIMADA"] = pd.to_numeric(df["POPULAÇÃO ESTIMADA"], errors="coerce")

# Estatística descritiva básica
estatisticas = df["POPULAÇÃO ESTIMADA"].describe()

# Conta valores ausentes
faltantes = df["POPULAÇÃO ESTIMADA"].isna().sum()

# Detecção de outliers usando método IQR
q1 = df["POPULAÇÃO ESTIMADA"].quantile(0.25)
q3 = df["POPULAÇÃO ESTIMADA"].quantile(0.75)
iqr = q3 - q1
limite_inferior = q1 - 1.5 * iqr
limite_superior = q3 + 1.5 * iqr

outliers = df[
    (df["POPULAÇÃO ESTIMADA"] < limite_inferior) |
    (df["POPULAÇÃO ESTIMADA"] > limite_superior)
]

# Consolida relatório em formato estruturado
relatorio = pd.DataFrame({
    "Métrica": [
        "Total de Municípios",
        "População Média",
        "População Mediana",
        "Desvio Padrão",
        "Mínimo",
        "Máximo",
        "1º Quartil",
        "3º Quartil",
        "Valores Ausentes",
        "Outliers Detectados"
    ],
    "Valor": [
        int(estatisticas["count"]),
        round(estatisticas["mean"], 2),
        round(estatisticas["50%"], 2),
        round(estatisticas["std"], 2),
        int(estatisticas["min"]),
        int(estatisticas["max"]),
        int(q1),
        int(q3),
        int(faltantes),
        len(outliers)
    ]
})

# Cria pasta se não existir
Path(output_path).parent.mkdir(parents=True, exist_ok=True)

# Salva relatório
relatorio.to_csv(output_path, index=False, encoding="utf-8")

# Exibe resumo no terminal
print("\n===== ESTATISTICA DESCRITIVA DA POPULACAO =====\n")
print(relatorio)
print("\nRelatorio salvo em:")
print(output_path)

# Fim do script
