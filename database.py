import mysql.connector
import pandas as pd

name_password = {
    "3306": "micontrasena",
    "3307": "contraslave1",
    "3308": "contraslave2",
    "3309": "contraslave3"
}

def connect_db(port):
    conn = mysql.connector.connect(
        user='root',
        password=name_password[port],
        host='localhost',
        port=port,
        database="replication_db"
    )
    return conn

def fetch_data(port, table):
    try:
        conn = connect_db(port)
        query = f"SELECT id, name FROM {table}"  
        df = pd.read_sql(query, conn)
        return df
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None
    finally:
        if 'conn' in locals() and conn.is_connected():
            conn.close()

def get_tables(port):
    try:
        conn = connect_db(port)
        query = "SHOW TABLES"
        df = pd.read_sql(query, conn)
        return df
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None
    finally:
        if 'conn' in locals() and conn.is_connected():
            conn.close()
