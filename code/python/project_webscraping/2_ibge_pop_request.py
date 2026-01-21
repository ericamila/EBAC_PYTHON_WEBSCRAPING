# PROJETO: Web Scraping de Dados Introdução 
# OBJETIVO: Coletar dados de Municípios do IBGE, por meio de requisição e armazená-los em um arquivo CSV.
# AUTOR: RODRIGO GARCIA BRUNINI
# DATA: 20/01/2026 
# VERSÃO: 1.0

# Metodologia:
"""
Este script realiza o download do arquivo original de estimativas populacionais do IBGE.

ETAPAS DO PROCESSO:
1. CONEXÃO: Estabelece conexão com o servidor FTP do IBGE
2. DOWNLOAD: Baixa o arquivo .xls em modo streaming (por partes) para economizar memória
3. ARMAZENAMENTO: Salva o arquivo localmente na pasta de dados brutos do projeto
4. VALIDAÇÃO: Verifica se o download foi concluído com sucesso

COMO USAR:
1. Instale a dependência: pip install requests
2. Execute o script: python baixar_xls_original.py
3. O arquivo será salvo em: C:/Users/<seu_usuario>/Desktop/projetos/data/raw/populacao.xls
   (a pasta é criada automaticamente se não existir)

FONTE DOS DADOS:
IBGE - Estimativas de População 2025
URL: https://www.ibge.gov.br/estatisticas/sociais/populacao/9103-estimativas-de-populacao.html?=&t=resultados

GLOSSÁRIO:
- FTP: Protocolo de transferência de arquivos (forma de baixar arquivos de servidores)
- Streaming: Download em partes pequenas, evitando sobrecarregar a memória
- chunk_size: Tamanho de cada parte baixada (8192 bytes = 8KB por vez)
- Path: Objeto que representa caminhos de arquivos de forma compatível com qualquer sistema operacional
- raise_for_status(): Verifica se houve erro no download e interrompe se necessário

OBSERVAÇÕES:
- Este script apenas baixa o arquivo original (.xls)
- Não realiza conversões ou transformações nos dados
- Se o arquivo já existir, será sobrescrito
- O arquivo baixado será usado como base para processamentos posteriores
"""

# Bibliotecas
from pathlib import Path
import requests

# URL direta do arquivo .xls (conforme indicado)
XLS_URL = "https://ftp.ibge.gov.br/Estimativas_de_Populacao/Estimativas_2025/POP2025_20260113.xls"

# Caminho onde o arquivo será salvo (ajuste se quiser outro local)
OUTDIR = Path.home() / "Desktop" / "ebac" / "EBAC_PYTHON_WEBSCRAPING" / "data" / "raw"
OUTDIR.mkdir(parents=True, exist_ok=True)
XLS_LOCAL = OUTDIR / "populacao.xls"

def download_xls_only(url: str, dest: Path, chunk_size: int = 8192):
    """
    Baixa o arquivo de 'url' em streaming e salva em 'dest'.
    Se já existir, será sobrescrito.
    """
    print(f"Baixando: {url}")
    resp = requests.get(url, stream=True, timeout=60)
    resp.raise_for_status()

    with open(dest, "wb") as f:
        for chunk in resp.iter_content(chunk_size=chunk_size):
            if chunk:
                f.write(chunk)

    print("Arquivo salvo em:", dest)
    return dest

def main():
    download_xls_only(XLS_URL, XLS_LOCAL)

if __name__ == "__main__":
    main()

# Fim do script #

