import psycopg2
from settings import *
from connection import Connection
import datetime


class SuperAdmin(Connection):

    def __init__(self, login, password):
        self.login = login
        self.password = password

    def add_admin(self, admin_data):
        if self.login_self():
            table = 'users'
            result = self._postData(table, admin_data)
        else:
            result = 'Incorrect login or password'
        return result


class Admin(Connection):

    def __init__(self, login, password):
        self.login = login
        self.password = password

    def login_self(self):
        return self._login_check(self.login, self.password)

    def add_pr_category(self, data):
        if self.login_self():
            table = 'product_category'
            result = self._postData(table, data)
        else:
            result = 'Incorrect login or password'
        return result

    def edit_pr_category(self, data, selector):
        if self.login_self():
            table = 'product_category'
            result = self._updateData(table, data, selector)
        else:
            result = 'Incorrect login or password'
        return result

    def delete_pr_category(self, selector):
        if self.login_self():
            table = 'product_category'
            selector = f"category_name = '{selector}'"
            result = self._deleteData(table, selector)
        else:
            result = 'Incorrect login or password'
        return result

    def get_order_info(self, category='', selector='',):
        """
        category must be one of the item from the list:
        ['date_of_order', 'code']
        date format for selector: 2020-6-12
        """
        if self.login_self():
            categoryes = ['date_of_order', 'code']
            table = ('orders o',)

            fields = ("""o.id, o.date_of_order, concat(u.first_name,' ', u.last_name) as "customer",
                         p.product_name as "product_name", p.code as "product_id", o.price, o.count, o.discount, o.total""",)
            fieldNames = ["id", "date_of_order", "customer",
                          "product_name", "product_id", "price", "count", "discount", "total"]
            if category and category in categoryes and selector != '':
                if isinstance(selector, bool):
                    where = f"""where {category} = {selector}"""
                else:
                    where = f"""where {category} = '{selector}'"""
            else:
                where = ''
            # print(where)
            selector = f""" left JOIN users u on u.id = o.customer_id
                            left JOIN product p on p.id = o.product_id 
                            {where}"""
            result = self._getData(table, fields, selector)
            changeRes = []
            for item in result:
                cort = {}
                for index, element in enumerate(item):
                    cort[fieldNames[index]] = element
                changeRes.append(cort)
        else:
            changeRes = 'Incorrect login or password'
        return changeRes


if __name__ == '__main__':

    admin_1_data = [{
        "first_name": "Bill",
        "last_name": "Bobb",
        "date_of_bitrth": "02.05.1684",
        "phone": "+803254",
        "address": "Streee1",
        "password": "123",
        "email": "opa@mail.dog",
        "role": "admin",
        "discount": "20"
    }]
    # ------------------------------------------------------
    # admin_1 = SuperAdmin('Bad', 'Bob').add_admin(admin_1_data)
    # ------------------------------------------------------
    admin_2 = Admin('opa@mail.dog', '123')
    admin_2.login_self

    rez = admin_2.get_order_info(category='code', selector='202154')
    print(rez)
    # ------------------------------------------------------
    rez = admin_2.get_order_info(
        category='date_of_order', selector='2021-09-2')
    print(rez)
    # ------------------------------------------------------
    # data = [{
    #     'category_name': "wardrobe"
    # }]
    # add = admin_2.add_pr_category(data)
    # print(add)
    # ------------------------------------------------------
    # data = {
    #     'category_name': "wardrobe"
    # }
    # edit = admin_2.edit_pr_category(data, "category_name = 'water'")
    # print(edit)
    # ------------------------------------------------------
    dele = admin_2.delete_pr_category('wardrobe')
    print(dele)
    # ------------------------------------------------------
