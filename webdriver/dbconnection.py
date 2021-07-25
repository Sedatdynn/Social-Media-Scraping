import mysql.connector

# Firstly , create schema named as, socialdatas.

def connect():
    my_db = mysql.connector.connect(
        user='sqlusername', # root
        password='sqlpassword', # 123456
        host='yourhost', # 127.0.0.1
        database='socialdatas',

    )

    return my_db

