
import os
from datetime import datetime

import scraper
from db import Dbinterface
from db.models import Publicacao_Original


def routine(*dates):

    results = _scrap_dates(dates)
    if len(results) == 0:
        return

    with Dbinterface(os.environ['DIARIOBOT_DATABASE_CONNECTIONSTRING']).opensession() as session:
        for publicacao in _get_publicacoes(results):
            entry = Publicacao_Original(**publicacao)
            session.add(entry)

        session.commit()

def _scrap_dates(dates):
    return scraper.scrap(dates[0]) + _scrap_dates(dates[1:]) if len(dates) > 0 else []

def _get_publicacoes(results):

    for result in results:
        edicao = { 'edicao': result['id'], 'numero': result['numero'], 'data': datetime.strptime(result['date'], '%Y-%m-%d').strftime('%d/%m/%Y') }

        for item in result['publicacoes']:
            summary = _get_summary(item['summary_stack'])
            publicacao = { 'materia': item['title'], 'identificador': item['identificador'], 'corpo': item['body'] }

            yield { **edicao, **summary, **publicacao, 'fonte': 'ioes' }

def _get_summary(summary_stack):

    if len(summary_stack) < 3:
        raise Exception('unsupported summary: {}'.format(summary_stack))

    categoria, orgao = summary_stack[:2]
    tipo, = summary_stack[-1:]
    suborgao = summary_stack[2] if len(summary_stack) > 3 else ''

    return { 'categoria': categoria, 'orgao': orgao, 'suborgao': suborgao, 'tipo': tipo }
