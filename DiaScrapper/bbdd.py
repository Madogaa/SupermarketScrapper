products = parse_dia()
#%%
products[::6]
# %%

import mysql.connector
from apireader import *
from scrapping import *

# Establecer la conexión con la base de datos
conn = mysql.connector.connect(
    host='143.47.50.240',
    port=3306,
    user='mario',
    password='Azarquiel2023',
    database='shopycheep'
)


# Crear un cursor para ejecutar consultas
cursor = conn.cursor()
try:
    query = "INSERT INTO producto (imagen,titulo,precio,precioporkilo,id_categoria,id_subcategoria ) VALUES (%s, %s, %s, %s, %s, %s)"
    for cat in products:
        values = (cat['Imagen'],cat['Titulo'],cat['Precio'],cat['PrecioPorKilo'],cat['idCategoria'],cat['idSubCategoria'])
        cursor.execute(query, values)
    conn.commit()

finally:
    conn.close()
# Confirmar los cambios en la base de datos


# Cerrar la conexión



# %%
