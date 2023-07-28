# %%
import urllib;
from bs4 import BeautifulSoup;
from selenium import webdriver
from selenium.webdriver.common.by import By


url = "https://www.condisline.com"


def get_links(url):
    response = urllib.request.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')
    links = soup.find_all('a', class_='submenu_link')
    return list(map(lambda a: a.get('href'), links))

def scrape_product_data(url,subcat):
    driver = webdriver.Chrome()  # Reemplaza esto con el controlador de tu navegador preferido

    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    product_data = []

    articles = soup.find_all('article', class_='article_container')
    for article in articles:
        # Obtener la imagen del producto
        image_url = article.find('img', class_='article_image')['data-original']

        # Obtener el título del producto
        title = article.find('span', id='description_text').text

        # Obtener el id del producto para buscar el precio específico
        product_id = article.find('span', id=lambda x: x and x.startswith('list_price_'))['id']

        # Buscar el precio usando el id del producto
        price = driver.find_element(By.ID, product_id).text.strip()

        # Obtener el precio por kilo o litro
        price_per_unit = article.find('div', class_='article_pum').text.strip()

        product_data.append({
            'subcategoria': subcat,
            'image_url': image_url,
            'title': title,
            'price': price,
            'price_per_unit': price_per_unit
        })

    driver.quit()
    return product_data

def condis_scraper(url):
    all_products=[]
    subcat = 185
    for link in get_links(url):
        all_products += scrape_product_data(url+link,subcat)
        subcat += 1

    return all_products

def data_clean(data):
    for product in data:
        product['price'] = product['price'].replace(',','.')
        product['price_per_unit'] = product['price_per_unit'].split('€/')[0]
        product['price_per_unit'] = product['price_per_unit'].replace(',','.')
        product['image_url'] = product['image_url'].replace('//','')

def to_float(product_data_list):
    for product in product_data_list:
        product['price'] = float(product['price'])
        if not isinstance(product['price_per_unit'],float) and product['price_per_unit'] != '':
            product['price_per_unit'] = float(product['price_per_unit'])
            print(product)
        else:
            if product['price_per_unit'] == '':
                product['price_per_unit'] = float(0.00)
                print(product)

def scrap_condis(url, product_data_list):
    product_data_list = condis_scraper(url)
    data_clean(product_data_list)
    to_float(product_data_list)




# %%
url = "https://www.condisline.com"

def scrape_categories_data(url):
    response = urllib.request.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')

    categories_data = []

    category_containers = soup.find_all('li', class_='menu_link_container')
    i=23
    for category_container in category_containers:
        # Obtener el título de la categoría
        category_title = category_container.find('span', class_='menu_link').text.strip()

        # Obtener las subcategorías de la categoría actual
        subcategories = category_container.find('div', class_='submenu').find_all('a', class_='submenu_link')
        subcategories_list = [subcategory.text.strip() for subcategory in subcategories]
        i += 1
        categories_data.append({
            'id_categoria': i ,
            'category_title': category_title,
            'subcategories': subcategories_list
        })

    return categories_data


categories_data_list = scrape_categories_data(url)
# Imprime los datos de las categorías y subcategorías obtenidas
for category_data in categories_data_list:
    print('id_categoria:', category_data['id_categoria'])
    print('Categoría:', category_data['category_title'])
    print('Subcategorías:', category_data['subcategories'])
    print('---')
# %%

# %%
