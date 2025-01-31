import requests
from bs4 import BeautifulSoup
import csv
import os
from urllib.parse import urljoin
import re
import pathlib
url_base = 'https://books.toscrape.com/index.html'
url_partiel ='https://books.toscrape.com/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
}

path = pathlib.Path(__file__).parent.resolve()

def parse_page(url):
    page = requests.get(url, headers=headers)
    page.encoding = 'utf-8'
    if page.status_code == 200:
        return BeautifulSoup(page.text, 'html.parser')
    return None

def extract_table_data(soup, field_name):
    th = soup.find_all('th')
    for i in th:
        if field_name in i.get_text():
            td = i.find_next('td')
            if td:
                return td.get_text()
            
def upc(soup):
    return extract_table_data(soup, 'UPC')

def title(soup):
    #Récupère le titre du livre et nettoie les caractères interdit dans le filename windows
    soup_title = soup.find('h1')
    raw_title = soup_title.get_text()
    title = re.sub(r'[*"/\\<>:|?]', '', raw_title)
    return title

def price_including_tax(soup):
    return extract_table_data(soup, 'Price (incl. tax)')

def price_excluding_tax(soup):
    return extract_table_data(soup, 'Price (excl. tax)') 
    
def availability(soup):
    return extract_table_data(soup, 'Availability')
                
def book_description(soup):
    #Récupère la description du livre
    product_description = soup.find(id='product_description')
    if product_description:
        p = product_description.find_next('p')
        return p.get_text()
    else:
        p = 'Aucune description'
        
def book_category(soup):
    #Récupère la categorie du livre
    breadcrumb = soup.find('ul', class_='breadcrumb').find_all('a')
    cat = breadcrumb[2]
    return cat.get_text()

def review_rating(soup):
    #Récupère le nombre d'étoiles (sur 5)
    star_rating = soup.find('div', class_='col-sm-6 product_main').find_all('p')
    rating = star_rating[2]
    number = rating.get('class')
    return number[1]
        
def image(soup):
    #Récupère l'url de l'image du livre
    url_class = soup.find('img')
    url_relative = url_class.get('src')
    url_complet = urljoin(url_base, url_relative)
    return url_complet

def csv_file_create(nom_categorie, path):
    #Crée un fichier csv 
    directory = os.path.join(path, f"databook\\{nom_categorie}")
    os.makedirs(directory, exist_ok=True)
    file_path = os.path.join(directory, nom_categorie + '.csv')
    with open (file_path, 'a', newline ='', encoding='utf-8') as file:
        writer = csv.writer(file)
        field = ['product_page_url', 'universal_product_code(upc)', 'title', 'price_including_tax', 'price_excludind_tax', 
        'number_available', 'product_description', 'category', 'review_rating','image_url']
        writer.writerow(field)

def add_data_csv(data, nom_categorie):
    #Ajoute les données au fichier csv
    directory = os.path.join(path, f"databook\\{nom_categorie}")
    file_path = os.path.join(directory, nom_categorie + '.csv')
    with open (file_path, 'a', newline = '', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(data)

def download_img(img_url, book_name, nom_categorie, path):
    #Télécharge l'image du livre à partir de son url
    response = requests.get(img_url)
    directory = os.path.join(path, f"databook\\{nom_categorie}\\images")
    os.makedirs(directory, exist_ok=True)
    img_path = os.path.join(directory, f'{book_name}.jpg')
    with open (img_path,'wb') as file:
        file.write(response.content)

def info_book(book_url, category, path):
    soup = parse_page(book_url)
    if soup:
        data = [book_url,
                upc(soup),
                title(soup),
                price_including_tax(soup),
                price_excluding_tax(soup),
                availability(soup),
                book_description(soup),
                book_category(soup),
                review_rating(soup),
                image(soup)]
        add_data_csv(data, category)
        download_img(image(soup), title(soup), book_category(soup), path)

def scrape_category(category_url, category, path):
    csv_file_create(category, path)
    page_number = 1
    while True:
        page_url = f"{category_url}/page-{page_number}.html" if page_number > 1 else category_url
        soup = parse_page(page_url)
        if not soup:
            break
        books = soup.find('ol', class_='row').find_all('h3')
        for book in books:
            relative_url = book.find('a')['href']
            url_book = urljoin(category_url, relative_url)
            info_book(url_book, category, path)
            page_number += 1
                
def scrape_all_category(url_base, url_partiel, path):
    soup = parse_page(url_base)
    nav_list = soup.find('ul', class_='nav nav-list').find('ul')
    url_category = nav_list.find_all('a')
    if nav_list:
        for c in url_category:
            category = c.get('href')
            category_url = urljoin(url_partiel, category)
            category_name = c.get_text(strip=True)
            scrape_category(category_url, category_name, path)            

scrape_all_category(url_base, url_partiel, path)