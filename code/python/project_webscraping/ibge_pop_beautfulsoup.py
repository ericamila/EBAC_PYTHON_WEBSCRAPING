# language: python
"""
baixar_xls_bs4.py

- Acessa a página de estimativas do IBGE, encontra o link do arquivo Excel (.xls/.xlsx)
  e baixa o arquivo original para um diretório local.
- Usa BeautifulSoup para localizar links <a href="...">.

Dependências:
pip install requests beautifulsoup4
"""

from pathlib import Path
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re

PAGE_URL = "https://www.ibge.gov.br/estatisticas/sociais/populacao/9103-estimativas-de-populacao.html?=&t=resultados"
OUTDIR = Path.home() / "Desktop" / "ebac" / "EBAC_PYTHON_WEBSCRAPING" / "data" / "raw"
OUTDIR.mkdir(parents=True, exist_ok=True)

HEADERS = {"User-Agent": "ScriptIBGE/BS4 - contato: seu-email@exemplo.com"}

# opcional: padrão para preferir (ex.: "POP2025"); se None, pega primeiro .xls/.xlsx encontrado
PREFER_PATTERN = "POP2025"  # coloque None para não usar preferência

def find_excel_links(page_url):
    r = requests.get(page_url, headers=HEADERS, timeout=30)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")

    links = []
    for a in soup.find_all("a", href=True):
        href = a["href"].strip()
        # considerar só links que terminam em .xls ou .xlsx (case-insensitive)
        if re.search(r"\.xls(x)?($|\?)", href, flags=re.IGNORECASE):
            links.append(href)
    # retornar lista de hrefs (talvez relativos)
    return links

def choose_link(links, base_url, prefer_pattern=None):
    if not links:
        return None
    abs_links = [urljoin(base_url, href) for href in links]
    if prefer_pattern:
        # prioriza links cujo nome contenha o padrão (case-insensitive)
        for u in abs_links:
            if prefer_pattern.lower() in Path(urlparse(u).path).name.lower():
                return u
    # fallback: se houver vários, escolher o primeiro que contenha 'POP' ou o primeiro da lista
    for u in abs_links:
        name = Path(urlparse(u).path).name.lower()
        if "pop" in name:
            return u
    return abs_links[0]

def download_file(url, dest_path, chunk_size=8192):
    print("Baixando:", url)
    r = requests.get(url, stream=True, headers=HEADERS, timeout=60)
    r.raise_for_status()
    with open(dest_path, "wb") as f:
        for chunk in r.iter_content(chunk_size=chunk_size):
            if chunk:
                f.write(chunk)
    print("Salvo em:", dest_path)
    return dest_path

def main():
    print("Buscando links de Excel na página...")
    links = find_excel_links(PAGE_URL)
    if not links:
        print("Nenhum link .xls/.xlsx encontrado na página.")
        return

    chosen = choose_link(links, PAGE_URL, prefer_pattern=PREFER_PATTERN)
    if not chosen:
        print("Não foi possível escolher um link a partir das opções:", links)
        return

    filename = Path(urlparse(chosen).path).name
    out_path = OUTDIR / filename

    # baixar e salvar apenas o arquivo original .xls/.xlsx
    download_file(chosen, out_path)

if __name__ == "__main__":
    main()
