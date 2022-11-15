import scrapy
from scrapy.selector import Selector
from scraping_camara.factory.parlamentar_factory import parlamentarFactory
from scraping_camara.factory.fill_parlamentar import fill_parlamentar
from scraping_camara.utils.util import bill_parser
from scraping_camara.utils.util import get_number_from_text

class SpiderDeputadosSpider(scrapy.Spider):
    name = 'spider_deputados'
    allowed_domains = ['https://www.camara.leg.br']
    start_urls = []
    with open('./scraping_camara/links/lista_deputados_string_list.txt') as file:
        start_urls = [line.rstrip() for line in file]

    def parse(self, response):
        yield fill_parlamentar(parlamentarFactory('M'), response)
