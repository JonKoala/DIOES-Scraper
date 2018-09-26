#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import urllib.request
import json
from lxml import etree


##
#CONSTANTS

URL_GET_EDICOES = 'http://ioes.dio.es.gov.br/apifront/portal/edicoes/edicoes_from_data/'
URL_GET_PUBLICACOES_SUMMARY = 'http://ioes.dio.es.gov.br/portal/visualizacoes/view_html_diario/'
URL_GET_PUBLICACAO = 'http://ioes.dio.es.gov.br/apifront/portal/edicoes/publicacoes_ver_conteudo/'


##
#UTILS

def _request(url):
    return urllib.request.urlopen(url).read()

def _extract_node_resources(node):
    text = node.xpath('./span/text()')[0]
    text = _fix_encoding(text)
    subnodes = node.xpath('./ul/li')
    return text, subnodes

def _extract_text(html):
    return ''.join(html.itertext())

#TEXT

def _fix_encoding(text):
    text = str(text)
    return text.encode('latin-1').decode('utf-8')

def _clean_text(text):
    text = text.replace('\n', ' ').replace('\r', ' ')
    return ' '.join(text.split())


##
#PUBLIC

def get_edicoes(date):

    response = _request(URL_GET_EDICOES + date)

    #extracting data from responses
    parsed = json.loads(response)
    edicoes = [diario for diario in parsed.get('itens')]

    #formatting and returning data
    edicoes = [dict(edicao=str(edicao.get('id')), numero=str(edicao.get('numero')), data=edicao.get('data')) for edicao in edicoes]
    return edicoes

def get_publicacoes_data(edicao):

    response = _request(URL_GET_PUBLICACOES_SUMMARY + edicao)

    #extracting brute data from response
    parsed = etree.HTML(response)
    content = parsed.xpath('//*[@id=\'tree\']')[0]

    #extracting data from html
    publicacoes = []
    categorias = content.xpath('./li')

    for categoria in categorias:
        categoria_name, orgaos = _extract_node_resources(categoria)

        for orgao in orgaos:
            orgao_name, suborgaos = _extract_node_resources(orgao)

            for suborgao in suborgaos:
                suborgao_name, tipos = _extract_node_resources(suborgao)

                for tipo in tipos:
                    tipo_name, materias = _extract_node_resources(tipo)

                    for materia in materias:
                        try:
                            materia_name = materia.xpath('./span/a/text()')[0]
                            materia_name = _fix_encoding(materia_name)
                            identificador = materia.xpath('./span/a/@identificador')[0]

                            publicacoes.append(dict(categoria=categoria_name, orgao=orgao_name, suborgao=suborgao_name, tipo=tipo_name, materia=materia_name, identificador=identificador))
                        except:
                            continue

    return publicacoes

def get_publicacao_body(identificador):

    response = _request(URL_GET_PUBLICACAO + identificador)
    if not response.strip():
        return ''

    content = etree.HTML(response)
    lines = content.xpath('//p')

    lines = [_clean_text(_extract_text(line)) for line in lines]
    text = '\n'.join(lines)
    return text

def scrap(*args):
    dates = args if len(args) > 0 else [time.strftime('%Y-%m-%d')]

    edicoes = [edicoes for date in dates for edicoes in get_edicoes(date)]

    results = []

    #getting data about publicações
    for edicao in edicoes:
        publicacoes_data = get_publicacoes_data(edicao['edicao'])
        publicacoes_data = [{**edicao, **publicacao_data} for publicacao_data in publicacoes_data]
        results += publicacoes_data

    #getting the body of each publicação
    for result in results:
        result['corpo'] = get_publicacao_body(result['identificador'])

    return results
