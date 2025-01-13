import requests
from bs4 import BeautifulSoup
import csv
import os
from urllib.parse import urljoin
base_url = 'https://books.toscrape.com/'
url = 'https://books.toscrape.com/catalogue/do-androids-dream-of-electric-sheep-blade-runner-1_149/index.html'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
}

page = requests.get(url, headers=headers)
soup = BeautifulSoup(page.text, 'html.parser') 
th = soup.find_all('th')

def upc():
    for i in th:
        if 'UPC' in i.get_text():
            td = i.find_next('td')
            if td:
                return td.get_text()
            
def title():
    title = soup.find('h1')
    return title.get_text()

def price_including_tax():
    for i in th:
         if 'Price (incl. tax)' in i.get_text():
            td = i.find_next('td')
            if td:
                return td.get_text()
                
def price_excluding_tax():
    for i in th:
         if 'Price (excl. tax)' in i.get_text():
            td = i.find_next('td')
            if td:
                return td.get_text()
        
def availability():
    for i in th:
         if 'Availability' in i.get_text():
            td = i.find_next('td')
            if td:
                return td.get_text()
                
def description():
    product_description = soup.find(id='product_description')
    p = product_description.find_next('p')
    return p.get_text()
            
def category():
    breadcrumb = soup.find('ul', class_='breadcrumb').find_all('a')
    cat = breadcrumb[2]
    return cat.get_text()

def review_rating():
    star_rating = soup.find('div', class_='col-sm-6 product_main').find_all('p')
    rating = star_rating[2]
    number = rating.get('class')
    return number[1]
        
def image():
    url_class = soup.find('img')
    url_relative = url_class.get('src')
    url_complet = urljoin(base_url, url_relative)
    return url_complet
    

universal_product_code = upc()
title_book = title()
price_incl_tax = price_including_tax()
price_excl_tax = price_excluding_tax()
number_availab = availability()
descrip = description()
cat = category()
rating = review_rating()
url_image = image()

def csv_file():
    directory = os.path.expandvars(r'C:\Users\%username%\Desktop\Openclassrooms\P1')
    os.makedirs(directory, exist_ok=True)
    file_path = os.path.join(directory, 'book_data.csv')
    with open (file_path, 'w', newline ='', encoding='utf-8') as file:
        writer = csv.writer(file)
        field = ['product_page_url', 'universal_product_code(upc)', 'title', 'price_including_tax', 'price_excludind_tax', 
        'number_available', 'product_description', 'category', 'review_rating','image_url']
        writer.writerow(field)
        writer.writerow([url, universal_product_code, title_book, price_incl_tax, price_excl_tax, number_availab, descrip, cat, rating, url_image])
    
csv_file()