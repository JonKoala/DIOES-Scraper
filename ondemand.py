#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import scraper
from db import Dbinterface
from db.models import Publicacao_Original

import argparse
import calendar
import os


##
# Utils

def get_dates(year, month):
    num_days = calendar.monthrange(year, month)[1]
    return ['-'.join([str(year), str(month), str(day)]) for day in range(1, num_days+1)]


##
# Command line arguments

parser = argparse.ArgumentParser()
parser.add_argument('year', type=int, help='Year to scrap')
parser.add_argument('month', type=int, help='Month to scrap')

year = parser.parse_args().year
month = parser.parse_args().month


##
# Scrap routine

print('starting scraping routine')

publicacoes = []
dates = get_dates(year, month)
for date in dates:
    print('scraping {}'.format(date))
    publicacoes += scraper.scrap(date)


##
# Persist results

print('persisting on database')

dbi = Dbinterface(os.environ['DIARIOBOT_DATABASE_CONNECTIONSTRING'])
with dbi.opensession() as session:

    for publicacao in publicacoes:
        entry = Publicacao_Original(**publicacao)
        session.add(entry)

    session.commit()
