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
            print(name)
        except AttributeError as e:
            name = None
        try:
            price = soup.find('span', class_='price-value-string js-price-value-string').text.strip()
            print(price)
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

            # writer.writerow()

    def main(self):
        url = 'https://www.avito.ru/saratov/avtomobili/'
        all_links = self.get_All_Links(self.get_Html(url))
        for i in all_links:
            html = self.get_Html(i)
            data = self.get_Page_Data(html)
            self.write_csv(data)


class Wiki:

    def get_Html(self, url):
        try:
            r = requests.get(url)
            return r.text
        except ConnectionError as e:
            print("Error")

    def get_All_Links(self, html):
        soup = BeautifulSoup(html, 'lxml')
        cars = soup.find('ul', class_='mw-allpages-chunk').find_all('a')
        links = []
        for car in cars:
            link = 'https://ru.wikipedia.org' + car.get('href')
            links.append(link)
        return links

    def get_Page_Data(self, html):
        soup = BeautifulSoup(html, 'lxml')

        try:
            birthday = soup.find('span', class_='bday').text.strip()
            print(birthday)
        except AttributeError as e:
            birthday = None
        try:
            name = soup.find('h1', class_='firstHeading').text.strip()
            print(name)
        except AttributeError as e:
            name = None
        date = {
            'birthday': birthday,
            'name': name
        }
        return date

    def write_csv(self, data):
        with open('wiki.csv', 'a') as file:
            writer = csv.writer(file, delimiter=' ')
            writer.writerow((data['name'], data['birthday']))

    def main(self):
        url = 'https://ru.wikipedia.org/wiki/%D0%A1%D0%BB%D1%83%D0%B6%D0%B5%D0%B1%D0%BD%D0%B0%D1%8F:%D0%92%D1%81%D0%B5_%D1%81%D1%82%D1%80%D0%B0%D0%BD%D0%B8%D1%86%D1%8B/%D0%A4'
        all_links = self.get_All_Links(self.get_Html(url))
        for i in all_links:
            html = self.get_Html(i)
            data = self.get_Page_Data(html)
            self.write_csv(data)


# avito = Avito()
# avito.main()

wiki = Wiki()
wiki.main()
