import scrapy
import scraping_camara.utils.response_collector as rc
from scraping_camara.factory.parlamentar_factory import parlamentarFactory
from scraping_camara.factory.fill_parlamentar import fill_parlamentar

class SpiderDeputadasSpider(scrapy.Spider):
    name = 'spider_deputadas'
    allowed_domains = ['https://www.camara.leg.br']
    start_urls = []
    with open('./scraping_camara/links/lista_deputadas_string_list.txt') as file:
        start_urls = [line.rstrip() for line in file]

    def parse(self, response):
        yield fill_parlamentar(parlamentarFactory('F'), response)
