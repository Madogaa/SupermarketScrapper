#%%




#%%

import os
os.chdir(r'C:\Users\mario\OneDrive\Escritorio\ShopyCheep-Scraping\DiaScrapper')
import mysql.connector
from apireader import *
from scrapping import *
from bs4 import BeautifulSoup
from config import credenciales


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
    query = "INSERT INTO categoria (id_supermercado,titulo) VALUES (%s,%s)"
    for category_data in categories_data_list:
        values = (2,category_data['category_title'])
        cursor.execute(query, values)
    conn.commit()

finally:
    conn.close()
# Confirmar los cambios en la base de datos




# %%
