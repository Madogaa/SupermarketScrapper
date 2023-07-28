#%%

#%%
import os
os.chdir(r'C:\Users\mario\OneDrive\Escritorio\ShopyCheep-Scraping\CondisScrapper')
import mysql.connector
from apireader import *
from ..config import credenciales

# Establecer la conexión con la base de datos
conn = mysql.connector.connect(
    host=credenciales['ip'],
    port=3306,
    user=credenciales['user'],
    password=credenciales['password'],
    database='shopycheep'
)


# Crear un cursor para ejecutar consultas
cursor = conn.cursor()
try:
    query = "INSERT INTO producto (id_subcategoria,id_supermercado,titulo,imagen,precio,precioporkilo) VALUES (%s,%s,%s,%s,%s,%s)"
    for product in product_data_list:
        values = (product['subcategoria'],2,product['title'],product['image_url'],product['price'],product['price_per_unit'])
        cursor.execute(query, values)
    conn.commit()

finally:
    conn.close()

# %%
