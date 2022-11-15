# Web scraping em Python usando Scrapy (LAB03-CDD)

Este repositório realiza um web scraping em 
diversas páginas de deputados e deputadas da 
câmara legislativa para retornar informações 
dos mesmos.

## Dependências
* Scrapy 2.7.1
### Como instalar?
```shell
$ pip install scrapy
```

## Executando o crawler
Após ter instalado o `Scrapy` execute os seguintes comandos na raiz do projeto:
```shell
$ scrapy crawl spider_deputados -o deputados.csv -t csv
$ scrapy crawl spider_deputadas -o deputadas.csv -t csv
```
Após executar você terá os dois arquivos `csv` necessários para executar o notebook no Google Colab. Caso não queira rodar o comando, os dois arquivos estão disponíveis na pasta `output_csv`.