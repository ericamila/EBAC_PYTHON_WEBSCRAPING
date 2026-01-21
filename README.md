# EBAC Python Web Scraping

Projeto desenvolvido para coleta, tratamento e análise de dados populacionais dos municípios brasileiros utilizando Python e técnicas de Web Scraping.

## Objetivo

Coletar dados do IBGE por meio de API e Web Scraping, realizar o tratamento dos dados e gerar análises estatísticas e visuais sobre a população dos municípios do Brasil.

## Tecnologias utilizadas

- Python
- Requests
- BeautifulSoup
- Pandas
- Matplotlib
- GeoPandas

## Estrutura do projeto

code/python/project_webscraping/  
Scripts de coleta, tratamento e análise dos dados  

data/  
Bases de dados utilizadas no projeto  

graficos/  
Gráficos gerados a partir das análises  

ppt/  
Apresentação final do projeto  

## Funcionalidades

- Coleta de dados via API do IBGE  
- Web scraping de dados populacionais  
- Limpeza e tratamento dos dados  
- Análise estatística descritiva  
- Geração de gráficos  
- Visualização geográfica da população  

## Como executar o projeto

1. Instale as dependências:

pip install pandas requests beautifulsoup4 matplotlib geopandas

2. Execute os scripts na seguinte ordem:

1_ibge_municipios_api.py  
2_ibge_pop_request.py  
3_col_pop.py  
4_join_pop_mun.py  
5_descritiva.py  
6_graficos.py  
7_mapaBR.py  

---

Projeto desenvolvido como parte do curso de Ciência de Dados da EBAC.
