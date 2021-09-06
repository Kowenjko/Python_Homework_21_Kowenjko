import psycopg2
from settings import *


class Connection():

    @classmethod
    def _openDB(cls):
        connection = psycopg2.connect(user=USER, password=PASSWORD,
                                      host=HOST, port=PORT,
                                      database='mebli_db')
        cursor = connection.cursor()
        return connection, cursor

    @classmethod
    def _closeDB(cls, connection, cursor):
        cursor.close()
        connection.close()

    def _getData(self, table: tuple, fields: tuple, selector=''):
        connection, cursor = self._openDB()
        select_query = f"""SELECT {','.join(fields)} FROM {','.join(table)} {selector} order by id;"""
        cursor.execute(select_query)
        connection.commit()
        result = cursor.fetchall()
        self._closeDB(connection, cursor)
        return result

    def _postData(self, table, data: list):
        connection, cursor = self._openDB()
        next_id = self._getNextId(table)
        # print(next_id)
        fields = list(data[0].keys())
        fields.append('id')
        values = ''
        for row in data:
            value = f"""({','.join(map(lambda item: f"'{item}'" ,row.values()))}, {next_id}),"""
            next_id += 1
            values += value
        insert_query = f"""INSERT INTO {table} ({','.join(fields)}) VALUES {values[:-1]};"""
        cursor.execute(insert_query)
        connection.commit()
        self._closeDB(connection, cursor)
        return 'Insert done!', next_id-1

    def _updateData(self, table, data: dict, selector: str):
        connection, cursor = self._openDB()
        set_items = ''
        for key in data:
            set_items += f"{key} = '{data[key]}',"
        update_query = f"""UPDATE {table} SET {set_items[:-1]} WHERE {selector}"""
        cursor.execute(update_query)
        connection.commit()
        self._closeDB(connection, cursor)
        return 'Update done!'

    def _deleteData(self, table, selector=''):
        connection, cursor = self._openDB()
        delete_query = f"""DELETE FROM {table} WHERE {selector};"""
        cursor.execute(delete_query)
        connection.commit()
        self._closeDB(connection, cursor)
        return 'Item was deleted!'

    def _getNextId(self, table):
        table = (table,)
        fields = ('id',)
        if self._getData(table, fields) == []:
            return 1
        result = sorted(self._getData(table, fields))[-1][0]+1
        return result

    # def _register(self, login, password, role):
    #     data = [{
    #         'login': login,
    #         'password': password,
    #         'role': role
    #     }]
    #     find_login = self._getData(
    #         ('users',), ('login',), f" where login = '{login}'")
    #     if not find_login:
    #         self._postData('users', data)
    #         return True
    #     else:
    #         print('Login is exist!')
    #         return False

    def _login_check(self, email, password):
        find_email = self._getData(
            ('users',), ('*',), f" where email = '{email}'")
        if find_email and password == find_email[0][6]:
            return find_email[0][7]
        else:
            return False
