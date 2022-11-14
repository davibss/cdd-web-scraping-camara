import scrapy
from scrapy.selector import Selector
from scraping_camara.utils.util import bill_parser
from scraping_camara.utils.util import get_number_from_text

class SpiderDeputadasSpider(scrapy.Spider):
    name = 'spider_deputadas'
    allowed_domains = ['https://www.camara.leg.br']
    start_urls = []
    with open('./scraping_camara/links/lista_deputadas_string_list.txt') as file:
        start_urls = [line.rstrip() for line in file]

    def parse(self, response):
        deputada = {
            'nome': None,
            'genero': 'F',
            'presenca_plenario': None, 
            'ausencia_plenario': None,
            'ausencia_justificada_plenario': None,
            'presenca_comissao': None,
            'ausencia_comissao': None,
            'ausencia_justificada_comissao': None,
            'data_nascimento': None,
            'gasto_total_par': None,
            'gasto_jan_par': None,
            'gasto_fev_par': None,
            'gasto_mar_par': None,
            'gasto_abr_par' : None, 
            'gasto_mai_par': None,
            'gasto_jun_par': None,
            'gasto_jul_par': None,
            'gasto_ago_par': None,
            'gasto_set_par': None,
            'gasto_out_par': None,
            'gasto_nov_par': None,
            'gasto_dez_par': None,
            'gasto_total_gab': None,
            'gasto_jan_gab': None,
            'gasto_fev_gab': None,
            'gasto_mar_gab': None,
            'gasto_abr_gab': None,
            'gasto_mai_gab': None,
            'gasto_jun_gab': None,
            'gasto_jul_gab': None,
            'gasto_ago_gab': None,
            'gasto_set_gab': None,
            'gasto_out_gab': None,
            'gasto_nov_gab': None,
            'gasto_dez_gab': None,
            'salario_bruto': None,
            'quant_viagem': None
        }

        name = response.css("ul.informacoes-deputado").get()
        deputada['nome'] = Selector(text=name).xpath('//li[span[contains(., "Nome Civil")]]/text()').get().strip()
        deputada['data_nascimento'] = Selector(text=name).xpath('//li[span[contains(., "Data de Nascimento")]]/text()').get().strip()
        deputada['quant_viagem'] = int(response.css("div.beneficio__viagens>span::text").get())
        deputada['salario_bruto'] = bill_parser(Selector(text=response.body).xpath('//h3[contains(text(), "Salário mensal bruto")]/../a/text()').get())

        [presenca_plenario_body, presencia_comissao_body] = response.css("div.list-table>ul.list-table__content>li").getall()
        [presenca_dias_plenario, ausencias_justificadas_plenario, ausencias_nao_justificadas_plenario] = \
            Selector(text=presenca_plenario_body).xpath("//dd/text()").getall()
        [presenca_dias_comissao, ausencias_justificadas_comissao, ausencias_nao_justificadas_comissao] = \
            Selector(text=presencia_comissao_body).xpath("//dd/text()").getall()
        
        deputada['presenca_plenario'] = get_number_from_text(presenca_dias_plenario)
        deputada['ausencia_plenario'] = get_number_from_text(ausencias_nao_justificadas_plenario)
        deputada['ausencia_justificada_plenario'] = get_number_from_text(ausencias_justificadas_plenario)
        
        deputada['presenca_comissao'] = get_number_from_text(presenca_dias_comissao)
        deputada['ausencia_comissao'] = get_number_from_text(ausencias_nao_justificadas_comissao)
        deputada['ausencia_justificada_comissao'] = get_number_from_text(ausencias_justificadas_comissao)
        
        deputada['gasto_total_par'] = bill_parser(response.css("table[id=percentualgastocotaparlamentar]>tbody>tr>td::text").getall()[1])
        deputada['gasto_total_gab'] = bill_parser(response.css("table[id=percentualgastoverbagabinete]>tbody>tr>td::text").getall()[1])

        table_cota_parlamentar = response.css("table[id=gastomensalcotaparlamentar]>tbody>tr>td::text").getall()
        table_cota_gabinete = response.css("table[id=gastomensalverbagabinete]>tbody>tr>td::text").getall()
        for i in range(0, len(table_cota_parlamentar), 3):
            deputada[f"gasto_{table_cota_parlamentar[i].lower()}_par"] = bill_parser(table_cota_parlamentar[i+1])
        for i in range(0, len(table_cota_gabinete), 3):
            deputada[f"gasto_{table_cota_gabinete[i].lower()}_gab"] = bill_parser(table_cota_gabinete[i+1])

        yield deputada
