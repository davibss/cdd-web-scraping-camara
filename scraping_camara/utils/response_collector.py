from scrapy.selector import Selector
from scraping_camara.utils.util import bill_parser, get_number_from_text

def get_name_from_response(response):
    base_info = response.css("ul.informacoes-deputado").get()
    return Selector(text=base_info).xpath('//li[span[contains(., "Nome Civil")]]/text()')\
        .get().strip()

def get_data_nascimento_from_response(response):
    base_info = response.css("ul.informacoes-deputado").get()
    return Selector(text=base_info)\
        .xpath('//li[span[contains(., "Data de Nascimento")]]/text()').get().strip()

def get_quant_viagem_from_response(response):
    return int(response.xpath('//div[@class="beneficio beneficio__viagens"]')\
        .xpath('*/text()').getall()[1])

def get_salario_bruto(response):
    return bill_parser(Selector(text=response.body)\
        .xpath('//h3[contains(text(), "Salário mensal bruto")]/../a/text()').get())

def get_presenca(response):
    result = {}
    presenca_table = response.css("div.list-table>ul.list-table__content>li").getall()
    if presenca_table != []:
        [presenca_plenario_body, presencia_comissao_body] = presenca_table
        plenario = Selector(text=presenca_plenario_body).xpath("//dd/text()").getall()
        comissao = Selector(text=presencia_comissao_body).xpath("//dd/text()").getall()
        result['plenario'] = {
            'presenca_dias_plenario': get_number_from_text(plenario[0]),
            'ausencias_justificadas_plenario': get_number_from_text(plenario[1]),
            'ausencias_nao_justificadas_plenario': get_number_from_text(plenario[2])
        }
        result['comissao'] = {
            'presenca_dias_comissao': get_number_from_text(comissao[0]),
            'ausencias_justificadas_comissao': get_number_from_text(comissao[1]),
            'ausencias_nao_justificadas_comissao': get_number_from_text(comissao[2])
        }
        
    return result

def get_gasto_total_par_from_response(response):
    return bill_parser(response.css("table[id=percentualgastocotaparlamentar]>tbody>tr>td::text")\
        .getall()[1])

def get_gasto_total_gab_from_response(response):
    return bill_parser(response.css("table[id=percentualgastoverbagabinete]>tbody>tr>td::text")\
        .getall()[1])

def get_gasto_mensal_from_response(response):
    result = {
        'parlamentar': {},
        'gabinete': {}
    }
    table_cota_parlamentar = response.css("table[id=gastomensalcotaparlamentar]>tbody>tr>td::text").getall()
    table_cota_gabinete = response.css("table[id=gastomensalverbagabinete]>tbody>tr>td::text").getall()
    for i in range(0, len(table_cota_parlamentar), 3):
        result['parlamentar'][f"gasto_{table_cota_parlamentar[i].lower()}_par"] = \
            bill_parser(table_cota_parlamentar[i+1])
    for i in range(0, len(table_cota_gabinete), 3):
        result['gabinete'][f"gasto_{table_cota_gabinete[i].lower()}_gab"] = \
            bill_parser(table_cota_gabinete[i+1])

    return result


