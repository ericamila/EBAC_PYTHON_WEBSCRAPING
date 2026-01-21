# PROJETO: Web Scraping de Dados Introdução 
# OBJETIVO: Coletar dados de Municípios do IBGE, por meio da API e armazená-los em um arquivo CSV.
# AUTOR: RODRIGO GARCIA BRUNINI
# DATA: 20/01/2026 
# VERSÃO: 1.0

# Instalar bibliotecas necessárias:
# pip install requests pandas

# Metodologia:
"""
Este script coleta a lista completa de municípios brasileiros diretamente da API oficial do IBGE.

ETAPAS DO PROCESSO:
1. REQUISIÇÃO: Acessa a API pública do IBGE para baixar dados de todos os municípios
2. EXTRAÇÃO: Processa o JSON retornado e extrai informações relevantes
3. ESTRUTURAÇÃO: Organiza os dados em colunas padronizadas (id_ibge, nome, uf_sigla, uf_nome, regiao)
4. VALIDAÇÃO: Trata valores ausentes e garante consistência dos dados
5. EXPORTAÇÃO: Salva o resultado final em arquivo CSV

COMO USAR:
1. Instale as dependências: pip install requests pandas
2. Execute o script: python webscraping_municipios.py
3. O arquivo será salvo em: C:/Users/<seu_usuario>/Desktop/projetos/data/raw/municipios.csv
   (a pasta é criada automaticamente se não existir)

FONTE DOS DADOS:
API oficial IBGE: https://servicodados.ibge.gov.br/api/docs/localidades

GLOSSÁRIO:
- API: Interface que permite acessar dados de forma automatizada
- JSON: Formato de dados estruturado (como uma árvore de informações)
- DataFrame: Tabela de dados organizada em linhas e colunas
- Endpoint: Endereço específico da API para acessar determinado tipo de dado
- safe_get: Função que busca dados aninhados sem gerar erros se algo estiver faltando

QUANDO USAR:
- Para obter a base atualizada de municípios brasileiros
- Quando precisar de dados geográficos oficiais do IBGE
- Para projetos que necessitam de códigos IBGE padronizados
"""

from pathlib import Path         # para lidar com caminhos de forma portátil
import requests                  # para fazer requisições HTTP
import pandas as pd              # para manipular e salvar tabelas
import os                        # para criar pastas se necessário
import time                      # para pausas curtas (boa prática)

# ----------- CONFIGURAÇÕES -------------

# Endpoint oficial do IBGE para lista de municípios
BASE_MUNICIPIOS = "https://servicodados.ibge.gov.br/api/v1/localidades/municipios"

# Cabeçalho HTTP: identificar seu script é permitido para o servidor
HEADERS = {"User-Agent": "ProjetoScrapingIBGE/ListaMunicipios/1.0 - contato: seu-email@exemplo.com"}

# Pasta de saída (ajuste se quiser outro local)
OUTDIR = Path.home() / "Desktop" / "ebac" / "EBAC_PYTHON_WEBSCRAPING" / "data" / "raw"
OUTFILE = OUTDIR / "municipios.csv"

# Pequena pausa entre operações (não estritamente necessária aqui, mas boa prática)
SLEEP = 0.1

# ---------------------------------------

def fetch_municipios():
    """
    Faz uma requisição GET ao endpoint de municípios do IBGE e retorna o JSON.
    Lança exceção se algo der errado (requests.raise_for_status()).
    """
    resp = requests.get(BASE_MUNICIPIOS, headers=HEADERS, timeout=20)
    resp.raise_for_status()   # se o status HTTP não for 200, lança erro com informação
    return resp.json()        # retorna lista de dicionários (cada dicionário = 1 município)

def safe_get(d, *keys, default=None):
    """
    Acessa chaves aninhadas com segurança.
    Ex.: safe_get(item, "microrregiao", "mesorregiao", "UF", "sigla")
    Retorna default se algum nível não for dict ou estiver ausente.
    """
    cur = d
    for k in keys:
        if not isinstance(cur, dict):
            return default
        cur = cur.get(k)
    return cur if cur is not None else default

def process_and_save(raw):
    """
    Processa o JSON bruto e salva o CSV com colunas:
    id_ibge, nome, uf_sigla, uf_nome, regiao
    """
    rows = []
    for item in raw:
        # id e nome são campos diretos
        cid = item.get("id")
        nome = item.get("nome")

        # uf/regiao estão aninhados na estrutura; usamos safe_get para evitar erros
        uf_sigla = safe_get(item, "microrregiao", "mesorregiao", "UF", "sigla")
        uf_nome = safe_get(item, "microrregiao", "mesorregiao", "UF", "nome")
        regiao = safe_get(item, "microrregiao", "mesorregiao", "UF", "regiao", "nome")

        rows.append({
            "id_ibge": str(cid) if cid is not None else None,  # padronizar como string
            "nome": nome,
            "uf_sigla": uf_sigla,
            "uf_nome": uf_nome,
            "regiao": regiao
        })

    # transformar em DataFrame e salvar CSV
    df = pd.DataFrame(rows)

    # garantir que a pasta exista
    os.makedirs(OUTDIR, exist_ok=True)

    # salvar CSV com encoding utf-8
    df.to_csv(OUTFILE, index=False, encoding="utf-8")
    return df

def main():
    print("🔍 Buscando lista de municípios do IBGE...")
    raw = fetch_municipios()

    # pequena pausa por educação (não necessária, mas mantém padrão)
    time.sleep(SLEEP)

    print(f" Total de registros recebidos: {len(raw)}")
    df = process_and_save(raw)

    print(" CSV salvo em:", OUTFILE)
    print(f" Total de municípios no CSV: {len(df)}")

if __name__ == "__main__":
    main()

# ----------- VERIFICAÇÃO DOS DADOS -------------

# Carrega o arquivo gerado para verificação
caminho_db = pd.read_csv(OUTFILE, encoding="utf-8")
df = caminho_db

# Exibe as primeiras linhas
print("\n Primeiras linhas do arquivo:")
print(df.head())

# Mostra informações sobre a estrutura dos dados
print("\n Informações sobre o dataset:")
print(df.info())

# Conta quantos estados únicos existem
print(f"\n Total de UFs (estados) únicos: {df['uf_nome'].nunique()}")

# Conta quantos municípios únicos existem
print(f"\n Total de municípios únicos: {df['nome'].nunique()}")

# Fim do script #
