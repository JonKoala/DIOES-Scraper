#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import scraper
import inout
from db import Dbinterface
from db.models import Publicacao, Publicacao_Original

import calendar
from datetime import date, timedelta
from sqlalchemy import desc


##
# Utils

def scrap(date):
    date_arg = date.strftime('%Y-%m-%d')
    return scraper.scrap(date_arg)


##
# Get resources

appconfig = inout.read_yaml('./appconfig')
dbi = Dbinterface(appconfig['db']['connectionstring'])

with dbi.opensession() as session:
    latest_update = session.query(Publicacao.data).order_by(desc(Publicacao.data)).first()[0]

#getting all dates between the latest update and today
delta = (date.today() - latest_update).days
dates = [latest_update + timedelta(days=i) for i in range(1, delta + 1)]


##
# Scrap routine

print('starting scraping routine')

publicacoes = []
for date in dates:
    print('scraping {}'.format(date))
    publicacoes += scrap(date)


##
# Persist results

print('persisting on database')

with dbi.opensession() as session:

    for publicacao in publicacoes:
        entry = Publicacao_Original(**publicacao)
        session.add(entry)

    session.commit()
