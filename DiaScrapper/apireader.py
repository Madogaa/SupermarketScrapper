# %%
import requests
import json

def get_categories():
    # Realizar la solicitud GET
    url = "https://www.dia.es/api/v1/plp-insight/initial_analytics/charcuteria-y-quesos/jamon-curado-y-paleta/c/L2004?filters=categories%3AL2004%3Aes&locale=es&navigation=L2004&page=1&seo=jam%C3%B3n+curado+y+paleta"
    response = requests.get(url)
    # Comprobar si la solicitud fue exitosa (código de estado 200)
    if response.status_code == 200:
        # Obtener el JSON de la respuesta
        json_data = response.json()

        # Acceder al objeto "menu_analytics"
        menu_analytics = json_data.get("menu_analytics")

        if menu_analytics:
            # Trabajar con los datos dentro de "menu_analytics"
            # Por ejemplo, imprimir el objeto completo
            return menu_analytics
        else:
            print("No se encontró el objeto 'menu_analytics' en el JSON.")
    else:
        print("La solicitud no fue exitosa. Código de estado:", response.status_code)

def category_links():
    menu_analytics = get_categories()
    # Lista para almacenar los valores de 'path'
    paths = []

    # Iterar sobre los objetos dentro de 'menu_analytics'
    for key, value in menu_analytics.items():
        # Verificar si el objeto tiene una clave 'children'
        if 'children' in value:
            # Iterar sobre los objetos dentro de 'children'
            for child_key, child_value in value['children'].items():
                # Verificar si el objeto hijo tiene una clave 'path'
                if 'path' in child_value:
                    # Agregar el valor de 'path' a la lista
                    paths.append(child_value['path'])

    return paths

def all_categories():
    paths = category_links()
    all_categories = []
    all_subcategories = []
    category_id = 1
    subcategory_id = 1
    category = paths[0].split('/')[1].replace('-', ' ')
    for path in paths:
        if category != path.split('/')[1].replace('-', ' '):
            Category = {
                'id': category_id,
                'titulo': category
            }
            all_categories.append(Category)
            category_id += 1

        Subcategory = {
            'id': subcategory_id,
            'idCategory' : category_id,
            'titulo': path.split('/')[2].replace('-', ' ')
        }
        all_subcategories.append(Subcategory)
        subcategory_id += 1

        category = path.split('/')[1].replace('-', ' ')
    return (all_categories,all_subcategories)

def find_category_id(categories, title):
    for category in categories:
        if category['titulo'] == title:
            return category['id'], category['idCategory']
    return None, None



# %%
