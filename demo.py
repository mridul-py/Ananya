import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Aditi@11",
        database="ananyadb",
        auth_plugin='mysql_native_password'
    )
