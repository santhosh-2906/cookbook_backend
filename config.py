import mysql.connector

def get_db_connection():
    connection = mysql.connector.connect(
        host="b7mhanlonjp5hn8uiuoy-mysql.services.clever-cloud.com",
        user="uh6jh8knswi9fpie",       
        password="YRRGCafTISFAdSJpqTeG", 
        database="b7mhanlonjp5hn8uiuoy"
    )
    return connection
