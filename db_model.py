"""
----------------------------------------
# ROLES
----------------------------------------
super_admin:
    # - create DB
    - create tables
    - add admin
    - login
admin:
    - fill tables
    - change data
    - delete data
    - get data by filter
    - login

unregistered_user:
    - register
    - get data by filter

registered_user
    - buy product
    - discount card
    - login
----------------------------------------
# DB model
----------------------------------------
users 
    - id
    - first_name
    - last_name
    - address
    - phone
    - birth_date
    - role
    - password
    - email
    - discount

products --> MEBLI
    - id
    - unique_code
    - name
    - price
    - count
    - description
    - image
    - SUB_category_id
----------------------------------------
МЕБЛІ>СТОЛИ>КУХОННІ>...
----------------------------------------
SUB_categories
    - id
    - name
    - categori_id

catrgories
    - id
    - name 
"""
