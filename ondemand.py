from datetime import date, timedelta
import calendar

from appconfig import settings
import db
import scraper


##
#UTILS

def get_dates(year, month):
    num_days = calendar.monthrange(year, month)[1]
    days = ['-'.join([str(year), str(month), str(day)]) for day in range(1, num_days+1)]

    return days

def save(dbinterface, data):
    dbinterface.insert(*data)
    dbinterface.commit()


##
#ROUTINE

dbi = db.factory.get_interface('publicacao')

year = 2016
month = 12
days = get_dates(year, month)

print('starting scraping routine')

#scraping and saving routine
for day in days:
    print('start scraping {}'.format(day))
    data = scraper.scrap(day)

    print('inserting to database')
    save(dbi, data)

print('scraping routine finished')
