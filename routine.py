import calendar
import datetime

from appconfig import settings
import scraper
import db


##
#CONSTANTS

YEAR = settings['routine']['year']
MONTH = settings['routine']['month']
DATABASE = settings['routine']['table']


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

dbinterface = db.factory.get_interface(DATABASE)

count_days = calendar.monthrange(YEAR, MONTH)[1]
days = [datetime.date(YEAR, MONTH, day+1) for day in range(count_days)]

for day in days:
    print('start scraping {}'.format(day))
    data = scrap(day)

    print('inserting to database')
    save(dbinterface, data)

print('scraping routine finished')
