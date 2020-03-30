
import asyncio
import functools
import json
from bs4 import BeautifulSoup

import scraper_web as webscraper


##
#CONSTANTS

URL_GET_EDICOES = 'http://ioes.dio.es.gov.br/apifront/portal/edicoes/edicoes_from_data/{date}'
URL_GET_PUBLICACOES_SUMMARY = 'http://ioes.dio.es.gov.br/portal/visualizacoes/view_html_diario/{id}'
URL_GET_PUBLICACAO = 'http://ioes.dio.es.gov.br/apifront/portal/edicoes/publicacoes_ver_conteudo/{identificador}'


##
# PUBLIC

def scrap(date):

    edicoes = get_edicoes(date)
    edicoes_with_summary_content = [{ **edicao, 'publicacoes': _get_summary_content(edicao['id']) } for edicao in edicoes]
    edicoes_with_publicacoes = [{ **edicao, 'publicacoes': _get_publicacoes(edicao['publicacoes']) } for edicao in edicoes_with_summary_content]

    return edicoes_with_publicacoes

def get_edicoes(date):

    response = webscraper.request(URL_GET_EDICOES.format(date=date))
    parsed_response = json.loads(response)

    return [{ 'id': item['id'], 'numero': item['numero'], 'date': date } for item in parsed_response['itens']]

def _get_summary_content(id):

    # parse summary content
    response = webscraper.request(URL_GET_PUBLICACOES_SUMMARY.format(id=id))
    tree = BeautifulSoup(response, 'html.parser')

    # return publicacoes extracted from the tree
    publicacoes_details = _get_publicacoes_details(tree)
    return publicacoes_details

def _get_publicacoes_details(node):

    # check if this node has children
    if node.ul:
        children = node.ul.find_all('li', recursive=False)

        # go deeper until i get to the leaf nodes
        children_leaves = [_get_publicacoes_details(child) for child in children]
        leaves = functools.reduce(lambda x, y: x + y, children_leaves if children_leaves else [[]])

        # update leaves' summary stack with this node's text (if any)
        node_text = [node.span.text] if node.find('span', recursive=False) else []
        updated_leaves = [{ **leaf, 'summary_stack': node_text + leaf['summary_stack'] } for leaf in leaves]

        return updated_leaves

    # leaf node, return own content
    leaf = node.span.a
    leaf_content = { 'title': leaf.text.strip(), 'identificador': leaf['identificador'], 'summary_stack': [] }
    return [leaf_content]

def _get_publicacoes(publicacoes):

    publicacoes_urls = [URL_GET_PUBLICACAO.format(identificador=publicacao['identificador']) for publicacao in publicacoes]
    publicacoes_content = asyncio.run(_scrap_publicacoes(publicacoes_urls))

    publicacoes = [{ **publicacao, 'body': body } for publicacao, body in zip(publicacoes, publicacoes_content) ]

    return publicacoes

async def _scrap_publicacoes(urls):

    semaphore = asyncio.Semaphore(20)
    tasks = [_scrap_publicacao(url, semaphore) for url in urls]

    return await asyncio.gather(*tasks)

async def _scrap_publicacao(url, semaphore):

    async with semaphore:
        response = await webscraper.async_request(url)

        # if page content exists and is html, extract text from it
        if response:
            soup = BeautifulSoup(response, 'html.parser')
            return soup.body.get_text()
