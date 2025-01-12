import csv
import os
import requests
from bs4 import BeautifulSoup

directory = 'C:\Users\%username%\Desktop\Openclassrooms\P1'
csv_path = os.path.join(directory, 'book_data')
url = 'https://books.toscrape.com/catalogue/do-androids-dream-of-electric-sheep-blade-runner-1_149/index.html'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
}

page = requests.get(url, headers=headers)
soup = BeautifulSoup(page.text, 'html.parser')

def upc():
    th = soup.find('th')
    
    if th and 'UPC' in th.get_text():
        td = soup.find('td')
        if td:
            print(td.get_text())

td_elements = soup.find_all('td')

csv_file = open(csv_path, 'w', encoding='utf-8', newline='')
writer = csv.writer(csv_file)

writer.writerow(['product_page_url', 'universal_product_code(upc)', 'title', 'price_including_tax', 'price_excludind_tax', 'number_available', 'product_description', 'category', 'review_rating','image_url'])
