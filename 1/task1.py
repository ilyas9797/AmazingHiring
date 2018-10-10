import csv
import sqlite3
import os
import logging


class Table:

    def __form_SQL_request__(self, command, args):
        '''
        Возвращает строку с запросом к БД. В зависимости от command содает запрос CREATE TABLE или INSERT
        '''
        if command == 'CREATE':
            request = f'CREATE TABLE {self._table_name} ('

            # В зависимости от именования атрибута, ему будет присвоен подходящий тип
            schema = ''
            for i in args:
                # В модуле SQLite3 нативно поддерживаются типы: NULL, INTEGER, REAL, TEXT, BLOB
                # Тип TIMESTAMP поддерживается, т.к. в csv-файле соответсвующие поля записаны в формате ISO timestamps
                if i.upper().find('DATE') >= 0:
                    schema += f"'{i}'" + ' TIMESTAMP, '
                elif i.upper().find('ID') >= 0:
                    schema += f"'{i}'" + ' INTEGER, '
                else:
                    schema += f"'{i}'" + ' TEXT, '
            schema = schema[:-2]
            
            logging.info(f"Table schema is: {schema}")

            request = request + schema + ');'
            return request

        if command == 'INSERT':
            # (SQLite documentation) A string constant is formed by enclosing the string in single quotes ('). A single quote within the string can be encoded by putting two single quotes in a row - as in Pascal. C-style escapes using the backslash character are not supported because they are not standard SQL.
            return f'INSERT INTO {self._table_name} VALUES (' + ', '.join("'{}'".format(i.replace("'", "''")) for i in args) + ');'

    def __init__(self,
                 schema,
                 db_file_name,
                 table_name='main_table'):
        self._table_name = table_name
        self._connection = sqlite3.connect(db_file_name)

        logging.info(f"Data base created in file '{db_file_name}'")

        self._cursor = self._connection.cursor()
        self._cursor.execute(self.__form_SQL_request__('CREATE', schema))

        logging.info(f"Table '{self._table_name}' created")
        

        self._counter = 0

    def add(self, row):
        self._cursor.execute(self.__form_SQL_request__('INSERT', row))
        self._counter += 1

    def end_writing(self):
        self._connection.commit()
        logging.info(f"Commited {self._counter} rows")

        self._connection.close()
        logging.info(f"Connection closed")


if __name__ == '__main__':

    def get_file_path(file):
        '''
        Возвращает путь до файла file, лежащего в той же директории что и скрипт
        '''
        return os.path.dirname(os.path.abspath(__file__)) + os.path.normpath(f'/{file}')

    def input_file_name(promt, default):
        '''
        Ввод аргументов, если ничего не введено, будет возвращено значение по умолчанию default
        '''
        file_name = input(promt)
        if not file_name:
            file_name = default
        return get_file_path(file_name)

    print('All files will be saved in the same directory where script is located')
    print('So type valid names for files (without path)\n')

    db_file = input_file_name(
        'Enter db file name (leave empty for default value):  ', 'police-department-calls-for-service.db')
    csv_file = input_file_name(
        'Enter csv file name (leave empty for default value): ', 'police-department-calls-for-service.csv')

    log_file = get_file_path('LOG.txt')
    FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
    logging.basicConfig(filename=log_file, filemode='w', level=logging.INFO, format=FORMAT)

    with open(csv_file, 'r') as file:

        logging.info(f"File '{csv_file}' opened")

        csv_records = csv.reader(file)
        table_schema = next(csv_records)
        my_table = Table(table_schema, db_file)

        for record in csv_records:
            my_table.add(record)

        my_table.end_writing()
