
import os
from datetime import date, timedelta
from sqlalchemy import desc

from db import Dbinterface
from db.models import Publicacao
from routine import routine as scrap_routine


dbi = Dbinterface(os.environ['DIARIOBOT_DATABASE_CONNECTIONSTRING'])
with dbi.opensession() as session:
    latest_update = session.query(Publicacao.data).filter(Publicacao.fonte == 'ioes').order_by(desc(Publicacao.data)).first()[0]

# getting all dates between the latest update and today
delta = (date.today() - latest_update).days
dates = [(latest_update + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(1, delta + 1)]

for scrap_date in dates:
    scrap_routine(scrap_date)
