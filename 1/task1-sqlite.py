import csv
import sqlite3


class Table:
    _table_schema = '{} INTEGER PRIMARY KEY, ' + 12 * '{} VARCHAR,' + ' {} VARCHAR'
    sql_command_create_table = 'CREATE TABLE {} (' + _table_schema + ');'
    sql_command_add_row_db = 'INSERT INTO {} VALUES ' + '(' + 13 * '\"{}\", ' + ' \"{}\");'
    _counter = 0

    def __init__(self,
                 table_schema,
                 log,
                 table_name='main_table',
                 db_file_name='police-department-calls-for-service.db'):
        self._table_name = table_name
        self._connection = sqlite3.connect(db_file_name)
        self._log = log
        self._log.write(f"Data base created in file '{db_file_name}'\n")
        self._cursor = self._connection.cursor()
        self._cursor.execute(
            self.sql_command_create_table.format(self._table_name, *table_schema))
        self._log.write(f"Table '{self._table_name}' created\n")
        self._log.write(f"Table schema: '{self._table_schema.format(*table_schema)}'\n")

    def add(self, row):
        try:
            self._cursor.execute(
                self.sql_command_add_row_db.format(self._table_name, *row))
        except sqlite3.OperationalError:
            self._log.write(f"There was OperationalError exeption with row:     {row}\n")
            row = list(map(lambda x: x.replace('"', '""'), row))
            self._log.write(f"OperationalError exeption corrected, changed row: {row}\n")
            self._cursor.execute(
                self.sql_command_add_row_db.format(self._table_name, *row))
        finally:
            self._counter += 1

    def end_writing(self):
        self._connection.commit()
        self._log.write(f"Commited {self._counter} rows\n")
        self._connection.close()
        self._log.write(f"Connection closed\n")


if __name__ == '__main__':

    log_path = './LOG.txt'
    with open(log_path, 'w') as log:
        db_file_name = 'police-department-calls-for-service.db'
        records_path = './police-department-calls-for-service.csv'
        with open(records_path, 'r') as file:
            log.write(f"File '{records_path} opened'\n")
            reader = csv.reader(file)
            table_schema = list(
                map(lambda x: x.replace(' ', ''), next(reader)))
            my_table = Table(table_schema, log, db_file_name=db_file_name)
            i = 10
            error_rows = []
            for row in reader:
                my_table.add(row)
            my_table.end_writing()
