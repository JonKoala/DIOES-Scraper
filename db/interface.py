import db.connection as connection
import db.sql_baker as baker

class Interface:

    def __init__(self, table, columns):
        self.table = table
        self.columns = columns

        self.cursor = connection.cursor


    #PUBLIC

    def commit(self):
        self.cursor.commit()

    def insert(self, *data_list):

        for data in data_list:
            query = baker.insert(self.table, data)
            self.cursor.execute(query)

    def select(self, *conditions, operator='OR'):

        query = baker.select(self.table, conditions, operator)

        result = self.cursor.execute(query)
        entries = result.fetchall()

        results = [self._dictionarify_row(entry) for entry in entries]
        return results


    #UTILS

    def _dictionarify_row(self, row_values):
        return dict(zip(self.columns, row_values))
