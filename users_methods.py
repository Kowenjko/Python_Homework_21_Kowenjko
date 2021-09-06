import psycopg2
from settings import *
from connection import Connection
from datetime import datetime


class Unregistered(Connection):

    def add_customer(self, customer_data):
        table = 'users'
        result = self._postData(table, customer_data)
        return result

    def get_product_info(self, category='', selector='',):
        """
        category must be one of the item from the list:
        ['product_name', 'code']        
        """
        categoryes = ['product_name', 'code']
        table = ('product p',)

        fields = (
            """p.id, p.code, p.product_name, ps.subcategory_name, pc.category_name, p.description, p.img, p.unit_price, p.count""",)
        fieldNames = ["id", "code", "product_name", "subcategory_name",
                      "category_name", "description", "img", "price", "count"]
        if category and category in categoryes and selector != '':
            if isinstance(selector, bool):
                where = f"""where {category} = {selector}"""
            else:
                where = f"""where {category} = '{selector}'"""
        else:
            where = ''
        selector = f""" left join product_subcategory ps on ps.id  = p.sub_category_id 
                        left  join product_category pc on pc.id = ps.category_id 
                        {where}"""
        result = self._getData(table, fields, selector)
        changeRes = []
        for item in result:
            cort = {}
            for index, element in enumerate(item):
                cort[fieldNames[index]] = element
            changeRes.append(cort)
        return changeRes


class Registered(Connection):
    def __init__(self, login, password):
        self.login = login
        self.password = password
        self._id = ''

    def login_self(self):
        email = self._login_check(self.login, self.password)
        if id:
            self._id = self._getData(
                ('users',), ('id',), f"where email = '{email}'")[0][0]
            return True
        return False

    def buy_product(self, products):
        if self.login_self():
            table = 'orders'
            data = []
            for item in products:
                discount = self._getData(
                    ('users',), ('discount',), f"where id = '{self._id}'")[0][0]
                order = {
                    "date_of_order": datetime.today().strftime('%Y-%m-%d'),
                    "customer_id": self._id,
                    "product_id": self._getData(('product',), ('id',), f"where code = '{item[0]}'")[0][0],
                    "price": self._getData(('product',), ('unit_price',), f"where code = '{item[0]}'")[0][0],
                    "count": item[1],
                    "discount": discount,
                    "total": self._getData(('product',), ('unit_price',), f"where code = '{item[0]}'")[0][0]*item[1]*(1-discount/100),
                }
                data.append(order)
            result = self._postData(table, data)
            return result
        else:
            result = 'Incorrect login or password'
        return result

    def discount_card(self):

        if self.login_self():
            table = ('users',)
            fields = ("""id, first_name ,last_name, discount""",)
            fieldNames = ["id", "first_name", "last_name", "discount"]
            selector = f""" where id= {self._id}"""
            result = self._getData(table, fields, selector)
            if not result == []:
                changeRes = []
                for item in result:
                    cort = {}
                    for index, element in enumerate(item):
                        cort[fieldNames[index]] = element
                    changeRes.append(cort)
            else:
                changeRes = 'You have no orders'

        else:
            changeRes = 'Incorrect login or password'
        return changeRes


if __name__ == '__main__':
    # -------------------------------------------------------
    # customer_1_data = [{
    #     "first_name": "Ronald",
    #     "last_name": "Reyn",
    #     "date_of_bitrth": "02.05.1689",
    #     "phone": "+803254256",
    #     "address": "Streee10",
    #     "password": "qwerty",
    #     "email": "ronald@gmail.com",
    #     "role": "customer",
    #     "discount": "10"
    # }]
    # customer_1 = Unregistered().add_customer(customer_1_data)
    # print(customer_1)
    # -------------------------------------------------------
    # customer_2 = Unregistered()

    # rez = customer_2.get_product_info(category='code', selector='202154')
    # print(rez)
    # -------------------------------------------------------
    reg_customer_1 = Registered('ronald@gmail.com', 'qwerty')
    # orders = reg_customer_1.buy_product(
    #     [('123456', 2), ('202154', 3)])
    # print(orders)
    # -------------------------------------------------------
    info = reg_customer_1.discount_card()
    print(info)
    # -------------------------------------------------------
