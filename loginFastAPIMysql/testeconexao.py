import pymysql

try:
    connection = pymysql.connect(
        host="localhost",
        user="root",
        password="root",
        database="usuarios_bd"
    )
    print("Conexão bem-sucedida!")
except Exception as e:
    print(f"Erro ao conectar: {e}")
