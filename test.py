import requests
from bs4 import BeautifulSoup
import csv
import os
from urllib.parse import urljoin

url_base = 'https://books.toscrape.com/index.html'
url_partiel ='https://books.toscrape.com/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
}

def upc(soup):
    th = soup.find_all('th')
    for i in th:
        if 'UPC' in i.get_text():
            td = i.find_next('td')
            if td:
                return td.get_text()
            
def title(soup):
    title = soup.find('h1')
    return title.get_text()

def price_including_tax(soup):
    th = soup.find_all('th')
    for i in th:
         if 'Price (incl. tax)' in i.get_text():
            td = i.find_next('td')
            if td:
                return td.get_text()
                
def price_excluding_tax(soup):
    th = soup.find_all('th')
    for i in th:
         if 'Price (excl. tax)' in i.get_text():
            td = i.find_next('td')
            if td:
                return td.get_text()
        
def availability(soup):
    th = soup.find_all('th')
    for i in th:
         if 'Availability' in i.get_text():
            td = i.find_next('td')
            if td:
                return td.get_text()
                
def description(soup):
    product_description = soup.find(id='product_description')
    p = product_description.find_next('p')
    return p.get_text()
            
def category(soup):
    breadcrumb = soup.find('ul', class_='breadcrumb').find_all('a')
    cat = breadcrumb[2]
    return cat.get_text()

def review_rating(soup):
    star_rating = soup.find('div', class_='col-sm-6 product_main').find_all('p')
    rating = star_rating[2]
    number = rating.get('class')
    return number[1]
        
def image(soup):
    url_class = soup.find('img')
    url_relative = url_class.get('src')
    url_complet = urljoin(url_base, url_relative)
    return url_complet

def csv_file(data):
    directory = os.path.expandvars(r'C:\Users\%username%\Desktop\Openclassrooms\P1')
    os.makedirs(directory, exist_ok=True)
    file_path = os.path.join(directory, 'book_data.csv')
    with open (file_path, 'a', newline ='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(data)
        
def info_book(category_url, headers):
    page_number = 1
    while True: 
        page_url = f"{category_url}/page-{page_number}.html" if page_number > 1 else category_url
        page = requests.get(page_url, headers=headers)
        soup = BeautifulSoup(page.text, 'html.parser')

        if page.status_code != 200:
            break
        
        soup = BeautifulSoup(page.text, 'html.parser')
        books = soup.find('ol', class_='row').find_all('h3')        
        
        for book in books:
            relative_url = book.find('a')['href']
            url_book = urljoin(category_url, relative_url)
            page = requests.get(url_book, headers=headers)
            if page.status_code == 200:
                soup = BeautifulSoup(page.text, 'html.parser')
                data = [url_book,
                upc(soup),
                title(soup),
                price_including_tax(soup),
                price_excluding_tax(soup),
                availability(soup),
                description(soup),
                category(soup),
                review_rating(soup),
                image(soup)]
                csv_file(data)
        page_number += 1            
                
def scrape_category(url_base, url_partiel, headers):
    #Création du fichier csv 
    directory = os.path.expandvars(r'C:\Users\%username%\Desktop\Openclassrooms\P1')
    os.makedirs(directory, exist_ok=True)
    file_path = os.path.join(directory, 'book_data.csv')
    
    #Création de l'en-tête
    with open (file_path, 'a', newline ='', encoding='utf-8') as file:
        writer = csv.writer(file)
        field = ['product_page_url', 'universal_product_code(upc)', 'title', 'price_including_tax', 'price_excludind_tax', 
        'number_available', 'product_description', 'category', 'review_rating','image_url']
        writer.writerow(field)
        
    #Parse la page d'acceuil du site   
    page = requests.get(url_base, headers=headers)
    soup = BeautifulSoup(page.text, 'html.parser')
    
    #Cherche les catégories et leurs liens partiels
    nav_list = soup.find('ul', class_='nav nav-list').find('ul')
    url_category = nav_list.find_all('a')
    
    #Pour chaque lien partiel, le rendre complet
    if nav_list:
        for category in url_category:
            cat = category.get('href')     
            category_url = urljoin(url_partiel, cat)
            #print (category_url)
            nom_categorie = category.get_text(strip=True)
            print (nom_categorie)
            #info_book(category_url, headers)

        
scrape_category(url_base, url_partiel, headers)
