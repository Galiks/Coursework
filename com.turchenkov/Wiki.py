import csv
import datetime
import re
from time import time
from multiprocessing import Pool

import os
from bs4 import BeautifulSoup
from pip._vendor import requests


class Wiki:
    path = ""

    def __init__(self):
        self.path = f"Pool/{str(datetime.datetime.now())[:19].replace(':', '.')}"
        os.mkdir(self.path)

        url = 'https://ru.wikipedia.org/wiki/%D0%A1%D0%BB%D1%83%D0%B6%D0%B5%D0%B1%D0%BD%D0%B0%D1%8F:%D0%92%D1%81%D0%B5_%D1%81%D1%82%D1%80%D0%B0%D0%BD%D0%B8%D1%86%D1%8B/%D0%A4'
        my_wiki_pages = [url]
        self.get_All_Links_On_Wiki(self.get_Html(url), my_wiki_pages)
        print("End. Pages were visited: " + str(len(my_wiki_pages)))

        with Pool(4) as first:
            first.map(self.make_link, my_wiki_pages)

    # exceprion_list = [
    #     'https://ru.wikipedia.org/wiki/%D0%A4%D0%B0%D1%82%D1%83%D0%BB%D0%BB%D0%B0%D0%B5%D0%B2,_%D0%A4%D0%B0%D1%82%D1%83%D0%BB%D0%BB%D0%B0_%D0%93%D0%B0%D0%BD%D0%B8_%D0%BE%D0%B3%D0%BB%D1%8B',
    #     'https://ru.wikipedia.org/wiki/%D0%A4%D0%B8%D1%88%D0%B0%D1%85_(%D0%B7%D0%BD%D0%B0%D1%87%D0%B5%D0%BD%D0%B8%D1%8F)']

    def give_date(self, birthday, name):
        if 1400 <= int(birthday[:4]) <= 1499:
            date15 = {
                'age': 15,
                'birthday': birthday,
                'name': name
            }
            self.write_csv15(date15)

        elif 1500 <= int(birthday[:4]) <= 1599:
            date16 = {
                'age': 16,
                'birthday': birthday,
                'name': name
            }
            self.write_csv16(date16)

        elif 1600 <= int(birthday[:4]) <= 1699:
            date17 = {
                'age': 17,
                'birthday': birthday,
                'name': name
            }
            self.write_csv17(date17)

        elif 1700 <= int(birthday[:4]) <= 1799:
            date18 = {
                'age': 18,
                'birthday': birthday,
                'name': name
            }
            self.write_csv18(date18)

        elif 1800 <= int(birthday[:4]) <= 1899:
            date19 = {
                'age': 19,
                'birthday': birthday,
                'name': name
            }
            self.write_csv19(date19)

        elif 1900 <= int(birthday[:4]) <= 1999:
            date20 = {
                'age': 20,
                'birthday': birthday,
                'name': name
            }
            self.write_csv20(date20)
        else:
            date = {
                'birthday': birthday,
                'name': name
            }
            self.write_csvElse(date)

    def write_csv15(self, data):
        with open(self.path + '/wiki15.csv', 'a') as file:
            writer = csv.writer(file, delimiter=' ')
            writer.writerow((data['name'], data['birthday']))

    def write_csv16(self, data):
        with open(self.path + '/wiki16.csv', 'a') as file:
            writer = csv.writer(file, delimiter=' ')
            writer.writerow((data['name'], data['birthday']))

    def write_csv17(self, data):
        with open(self.path + '/wiki17.csv', 'a') as file:
            writer = csv.writer(file, delimiter=' ')
            writer.writerow((data['name'], data['birthday']))

    def write_csv18(self, data):
        with open(self.path + '/wiki18.csv', 'a') as file:
            writer = csv.writer(file, delimiter=' ')
            writer.writerow((data['name'], data['birthday']))

    def write_csv19(self, data):
        with open(self.path + '/wiki19.csv', 'a') as file:
            writer = csv.writer(file, delimiter=' ')
            writer.writerow((data['name'], data['birthday']))

    def write_csv20(self, data):
        with open(self.path + '/wiki20.csv', 'a') as file:
            writer = csv.writer(file, delimiter=' ')
            writer.writerow((data['name'], data['birthday']))

    def write_csvElse(self, data):
        with open(self.path + '/wikiElse.csv', 'a') as file:
            writer = csv.writer(file, delimiter=' ')
            writer.writerow((data['name'], data['birthday']))

    def get_Html(self, url):
        try:
            r = requests.get(url)
            return r.text
        except ConnectionError as e:
            print("Error")

    def get_All_Links_On_Wiki(self, html, pages):
        soup = BeautifulSoup(html, 'lxml')
        wiki_pages = soup.find('div', class_='mw-allpages-nav').find_all('a')
        # if wiki_pages[1].text.find("Следующая страница (Х"):
        while len(pages) < 2:
            print(wiki_pages[1].text)
            page = 'https://ru.wikipedia.org' + wiki_pages[1].get('href')
            pages.append(page)
            self.get_All_Links_On_Wiki(self.get_Html(page), pages)

    def get_All_Links_On_Page(self, html):
        soup = BeautifulSoup(html, 'lxml')
        persons = soup.find('ul', class_='mw-allpages-chunk').find_all('a')
        links = []
        for person in persons:
            link = 'https://ru.wikipedia.org' + person.get('href')
            links.append(link)
        print("End. Pages were visited: " + str(len(links)))
        return links

    def get_Birthday(self, soup):
        try:
            birthday = soup.find('span', class_='bday').text.strip()
        except AttributeError as e:
            birthday = None
        return birthday

    def get_Name(self, soup):
        try:
            name = soup.find('h1', class_='firstHeading').text.strip()
        except AttributeError as e:
            name = None
        return name

    def get_Page_Data(self, html):
        soup = BeautifulSoup(html, 'lxml')
        birthday = self.get_Birthday(soup)
        if birthday is not None:
            if re.match(r"[0-9]{4}", birthday):
                name = self.get_Name(soup)
                if re.match(r"ФК", name):
                    print("Football club")
                elif re.match(r"Формула-1", name):
                    print("Formula-1")
                else:
                    print(name)
                    self.give_date(birthday, name)

    def make_link(self, url):
        link = self.get_All_Links_On_Page(self.get_Html(url))
        for i in link:
            self.make_data(i)

    def make_data(self, url):
        html = self.get_Html(url)
        self.get_Page_Data(html)


# main
if __name__ == '__main__':
    start_time = time()
    wiki = Wiki()
    print("Program's end")
    end_time = time()
    time_program = end_time - start_time
    file = open(wiki.path + "/Program's time.txt", 'w')
    file.write(str(time_program))
    file.close()
