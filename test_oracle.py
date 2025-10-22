import oracledb
import os

os.environ["TNS_ADMIN"] = "/Users/mac/Micro-servicio_Oracle/infra/wallet"

conn = oracledb.connect(
    user="TMDV",
    password="None00010001",
    dsn="reacttodosozzj_tp",
    config_dir="/Users/mac/Micro-servicio_Oracle/infra/wallet",
    wallet_location="/Users/mac/Micro-servicio_Oracle/infra/wallet",
    wallet_password="None00010001"
)
print("¡Conexión exitosa!")
conn.close()

