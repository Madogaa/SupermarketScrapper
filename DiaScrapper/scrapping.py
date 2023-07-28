#%%
import urllib;
from bs4 import BeautifulSoup;
from apireader import *


def get_soup(url):
    response = urllib.request.urlopen(url)
    html = response.read()
    return BeautifulSoup(html, 'html.parser')

def unique_parse(url):
    soup = get_soup('https://www.dia.es' + url)
    images = soup.find_all('img', class_='search-product-card__product-image')
    names = soup.find_all('p', class_='search-product-card__product-name')
    price = soup.find_all('p', class_='search-product-card__active-price')
    pricekilo = soup.find_all('p', class_='search-product-card__price-per-unit')

    src_list = list(map(lambda img: img.get('src'), images))
    name_list = list(map(lambda name: name.contents[0], names))
    price_list = list(map(lambda price: price.contents[0], price))
    pricekilo_list = list(map(lambda pricekilo: pricekilo.contents[0], pricekilo))


    idSubCategoria, idCategoria = find_category_id(all_categories()[1], url.split('/')[2].replace('-', ' '))

    all_products = {
        'Imagenes' : src_list ,
        'Titulos' : name_list,
        'Price' : price_list,
        'KiloPrice' : pricekilo_list
        }

    products= []
    for i in range(len(all_products['Titulos'])):
        producto = {
            'Imagen': all_products['Imagenes'][i],
            'Titulo': all_products['Titulos'][i],
            'Precio': all_products['Price'][i],
            'PrecioPorKilo': all_products['KiloPrice'][i],
            'idSubCategoria': idSubCategoria,
            'idCategoria' : idCategoria
        }
        products.append(producto)

    return products

def section_parse(url):
    soup = get_soup('https://www.dia.es' + url)

    next_pages = soup.find_all('a', class_='pagination-button__page--links')
    nextpages_list = list(map(lambda nextpages: nextpages.get('href'), next_pages))
    nextpages_list = [url] + nextpages_list

    section_products = []

    for page in nextpages_list:
        section_products = section_products + unique_parse(page)

    return section_products

def convert_to_float(price,titulo):
    try:
        price = price.replace('(', '')
        price = price.replace('\xa0€', '')
        price = price.replace(',', '.')
        price = price.split('/')[0]
        price = float(price)
        return(round(price,2))
    except ValueError as e:
        print(f"Error al convertir el precio a float: {e} ==> {titulo}" )
        # Puedes decidir cómo manejar el error aquí, por ejemplo, retornar un valor por defecto
        return float(0)  # O cualquier otro valor que consideres apropiado


def clean_products(productos):
    for product in productos:
        product['Precio'] = convert_to_float(product['Precio'],product['Titulo'])
        product['PrecioPorKilo'] = convert_to_float(product['PrecioPorKilo'],product['Titulo'])

def parse_dia():
    productos = []
    for url in category_links():
        productos = productos + section_parse(url)

    clean_products(productos)
    return productos

productos = parse_dia()
productos


# %%
