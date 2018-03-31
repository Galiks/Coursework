from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import requests
import csv
from datetime import datetime
from multiprocessing import Pool
import webbrowser as wb
from html.parser import HTMLParser
import re


class Avito:

    def get_Html(self, url):
        try:
            r = requests.get(url)
            return r.text
        except ConnectionError as e:
            print("Error")

    def get_All_Links(self, html):
        soup = BeautifulSoup(html, 'lxml')
        cars = soup.find('div', class_='js-catalog_after-ads').find_all('a', class_='item-description-title-link')
        links = []
        for car in cars:
            link = 'https://www.avito.ru' + car.get('href')
            links.append(link)
        return links

    def get_Page_Data(self, html):
        soup = BeautifulSoup(html, 'lxml')
        try:
            name = soup.find('span', class_='title-info-title-text').text.strip()
        except AttributeError as e:
            name = None
        try:
            price = soup.find('span', class_='price-value-string js-price-value-string').text.strip()
        except AttributeError as e:
            price = None
        date = {
            'name': name[:-6],
            'price': price[:-2]
        }
        return date

    def write_csv(self, data):
        with open('auto.csv', 'w') as file:
            writer = csv.writer(file)
            for line in data:
                print(line)

                # writer.writerow()

    def main(self):
        url = 'https://www.avito.ru/saratov/avtomobili/'
        all_links = self.get_All_Links(self.get_Html(url))
        for i in all_links:
            html = self.get_Html(i)
            data = self.get_Page_Data(html)
            self.write_csv(data)


class Test:
    html = urlopen("https://en.wikipedia.org/wiki/Kevin_Bacon")
    bs = BeautifulSoup(html, 'lxml')
    for link in bs.find("div", {"id": "bodyContent"}).find("a", href=re.compile("^(/wiki/)((?!:).)*$")):
        print(link)


avito = Avito()
avito.main()
test = Test()

