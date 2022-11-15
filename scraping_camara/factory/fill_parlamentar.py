import scraping_camara.utils.response_collector as rc

def fill_parlamentar(parlamentar, response):
    parlamentar['nome'] = rc.get_name_from_response(response)
    parlamentar['data_nascimento'] = rc.get_data_nascimento_from_response(response)
    parlamentar['quant_viagem'] = rc.get_quant_viagem_from_response(response)
    parlamentar['salario_bruto'] = rc.get_salario_bruto(response)

    presenca_result = rc.get_presenca(response)
    if presenca_result != {}:
        parlamentar['presenca_plenario'] = presenca_result['plenario']['presenca_dias_plenario']
        parlamentar['ausencia_plenario'] = presenca_result['plenario']['ausencias_justificadas_plenario']
        parlamentar['ausencia_justificada_plenario'] = presenca_result['plenario']['ausencias_nao_justificadas_plenario']
        parlamentar['presenca_comissao'] = presenca_result['comissao']['presenca_dias_comissao']
        parlamentar['ausencia_comissao'] = presenca_result['comissao']['ausencias_justificadas_comissao']
        parlamentar['ausencia_justificada_comissao'] = presenca_result['comissao']['ausencias_nao_justificadas_comissao']

    parlamentar['gasto_total_par'] = rc.get_gasto_total_par_from_response(response)
    parlamentar['gasto_total_gab'] = rc.get_gasto_total_gab_from_response(response)

    result_cota = rc.get_gasto_mensal_from_response(response)
    for key in result_cota['parlamentar']:
        parlamentar[key] = result_cota['parlamentar'][key]
    for key in result_cota['gabinete']:
        parlamentar[key] = result_cota['gabinete'][key]

    return parlamentar