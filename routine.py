from datetime import date, timedelta
import calendar

from appconfig import settings
import db
import scraper


##
#UTILS

def scrap(date):
    date_arg = date.strftime('%Y-%m-%d')
    data = scraper.scrap(date_arg)

    return data

def save(dbinterface, data):
    dbinterface.insert(*data)
    dbinterface.commit()


##
#ROUTINE

dbi_diario = db.factory.get_interface('publicacao')
dbi_latest_update = db.factory.get_interface('latest_publicacao')

startingdate = dbi_latest_update.select()[0]['data']

#getting all dates between starting date and today
delta = (date.today() - startingdate).days
days = [startingdate + timedelta(days=i) for i in range(1, delta + 1)]

print('starting scraping routine')

#scraping and saving routine
for day in days:
    print('start scraping {}'.format(day))
    data = scrap(day)

    print('inserting to database')
    save(dbi_diario, data)

print('scraping routine finished')
