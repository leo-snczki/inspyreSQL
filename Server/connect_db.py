
import mysql.connector

def start_connection():
    return mysql.connector.connect(
        host="127.0.0.1", # Endereço do servidor pelo zerotier ou localhost se rodar localmente cliente e servidor
        user="root",
        password="password",
        port=6033
    )

def start_connection_db():
    return mysql.connector.connect(
        host="127.0.0.1", # Endereço do servidor pelo zerotier ou localhost se rodar localmente cliente e servidor
        user="root",
        password="password",
        port=6033,
        database="hospytal_db"
    )
