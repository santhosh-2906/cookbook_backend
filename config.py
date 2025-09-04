import mysql.connector

def get_db_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",       
        password="Sandy@123", 
        database="cooking_notes"
    )
    return connection
