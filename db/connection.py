import pyodbc
from appconfig import settings


##
#PUBLIC

cnxn = pyodbc.connect(settings['db']['connectionstring'], autocommit=settings['db']['autocommit'])
cursor = cnxn.cursor()
