import requests
from bs4 import BeautifulSoup

url = 'https://books.toscrape.com/catalogue/do-androids-dream-of-electric-sheep-blade-runner-1_149/index.html'
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')

tr = soup.find_all('tr')
headers_csv = ['UPC', 'Price (incl. tax)', 'Availability']

for i in tr:
    th = i.find('th')
    for j in headers_csv:
     if th and j in th.get_text():
        td = i.find('td')
        if td:
            value = td.get_text()
            print (value)

