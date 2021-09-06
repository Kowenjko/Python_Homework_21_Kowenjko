from admin_methods import Admin
from admin_methods import SuperAdmin
from users_methods import Unregistered
from users_methods import Registered

from pprint import pprint
from custom import respprint
import datetime

# --------------------------------------------------------------------
admin_2 = Admin('opa@mail.dog', '123')
# rez = admin_2.get_order_info(category='code', selector='202154')
rez = admin_2.get_order_info(category='code', selector='')
respprint(rez)
# print(rez)
# --------------------------------------------------------------------
customer_2 = Unregistered()

rez = customer_2.get_product_info(category='code', selector='202154')
respprint(rez)
# print(rez)
# --------------------------------------------------------------------
reg_customer_1 = Registered('ronald@gmail.com', 'qwerty')
info = reg_customer_1.discount_card()
respprint(info)
# --------------------------------------------------------------------
