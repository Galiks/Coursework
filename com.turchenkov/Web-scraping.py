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


def get_Html(url):
    try:
        r = requests.get(url)
        return r.text
    except ConnectionError as e:
        print("Error")


def get_All_Links(html):
    soup = BeautifulSoup(html, 'lxml')
    cars = soup.find('div', class_='js-catalog_after-ads').find_all('a', class_='item-description-title-link')
    links = []
    for car in cars:
        link = 'https://www.avito.ru' + car.get('href')
        links.append(link)
    return links


def get_Page_Data(html):
    soup = BeautifulSoup(html, 'lxml')
    try:
        name = soup.find('h1', class_='title-info-title-text').text.strip()
    except AttributeError as e:
        name = None

    try:
        price = soup.find('span', class_='price-value-string js-price-value-string').text.strip()

    except AttributeError as e:
        price = None
    date = {
        'name': name,
        'price': price
    }

    return date


def write_csv(data):
    with open('auto.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerow((data['name'],
                         data['price']))
        print(data['name'], data['price'])


def main():
    url = 'https://www.avito.ru/saratov/avtomobili/'

    all_links = get_All_Links(get_Html(url))
    for i in all_links:
        html = get_Html(i)
        data = get_Page_Data(html)
        print(data['name'] + " : " + data['price'])
        #write_csv(data)


main()
