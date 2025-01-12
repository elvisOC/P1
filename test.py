import requests
from bs4 import BeautifulSoup
import csv
import os
import re
url = 'https://books.toscrape.com/catalogue/do-androids-dream-of-electric-sheep-blade-runner-1_149/index.html'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
}

# retrieving the target web page
page = requests.get(url, headers=headers)

soup = BeautifulSoup(page.text, 'html.parser')

#th_elements = soup.find_all('th')
#print (th_elements)

#td_elements = soup.find_all('td')
#print (td_elements)



#for tag in tr_elements:
 #   print(tag.get_text())
 
#title = soup.find('h1')
#print(title.get_text())
#csv_file = open(csv_path, 'w', encoding='utf-8', newline='')
#writer = csv.writer(csv_file)
#writer.writerow(['product_page_url', 'universal_product_code(upc)', 'title', 'price_including_tax', 'price_excludind_tax', 'number_available', 'product_description', 'category', 'review_rating','image_url'])
    
th = soup.find_all('th')

def upc():
    for i in th:
        if 'UPC' in i.get_text():
            td = i.find_next('td')
            if td:
                print(td.get_text())
            
def title():
    title = soup.find('h1')
    print (title.get_text())

def price_including_tax():
    for i in th:
         if 'Price (incl. tax)' in i.get_text():
            td = i.find_next('td')
            if td:
                print(td.get_text())
                
def price_excluding_tax():
    for i in th:
         if 'Price (excl. tax)' in i.get_text():
            td = i.find_next('td')
            if td:
                print(td.get_text())
        
def availability():
    for i in th:
         if 'Availability' in i.get_text():
            td = i.find_next('td')
            if td:
                print(td.get_text())
                


product_description = soup.find(id='product_description')
def description():
    for i in product_description:
        p = i.find_next('p')
        if p:
            print(p.get_text())
            

#breadcrumb = soup.find_all(class_='breadcrumb')
#category = breadcrumb.find_all('a')
breadcrumb = soup.find('ul', class_='breadcrumb').find_all('a')
#print (breadcrumb)

def category():
    cat = breadcrumb[2]
    print (cat.get_text())


def review_rating():
    star_rating = soup.find('div', class_='col-sm-6 product_main').find_all('p')
    rating = star_rating[2]
    number = rating.get('class')
    print (number[1])
        
    

#upc()
#title()
#price_including_tax()
#price_excluding_tax()
#availability()
#description()
#category()
review_rating()