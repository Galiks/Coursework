import csv
import re
from time import time

from pip._vendor import requests
from bs4 import BeautifulSoup


class Wiki:



    exceprion_list = [
        'https://ru.wikipedia.org/wiki/%D0%A4%D0%B0%D1%82%D1%83%D0%BB%D0%BB%D0%B0%D0%B5%D0%B2,_%D0%A4%D0%B0%D1%82%D1%83%D0%BB%D0%BB%D0%B0_%D0%93%D0%B0%D0%BD%D0%B8_%D0%BE%D0%B3%D0%BB%D1%8B',
        'https://ru.wikipedia.org/wiki/%D0%A4%D0%B8%D1%88%D0%B0%D1%85_(%D0%B7%D0%BD%D0%B0%D1%87%D0%B5%D0%BD%D0%B8%D1%8F)']

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
        with open('wiki15.csv', 'a') as file:
            writer = csv.writer(file, delimiter=' ')
            writer.writerow((data['name'], data['birthday']))

    def write_csv16(self, data):
        with open('wiki16.csv', 'a') as file:
            writer = csv.writer(file, delimiter=' ')
            writer.writerow((data['name'], data['birthday']))

    def write_csv17(self, data):
        with open('wiki17.csv', 'a') as file:
            writer = csv.writer(file, delimiter=' ')
            writer.writerow((data['name'], data['birthday']))

    def write_csv18(self, data):
        with open('wiki18.csv', 'a') as file:
            writer = csv.writer(file, delimiter=' ')
            writer.writerow((data['name'], data['birthday']))

    def write_csv19(self, data):
        with open('wiki19.csv', 'a') as file:
            writer = csv.writer(file, delimiter=' ')
            writer.writerow((data['name'], data['birthday']))

    def write_csv20(self, data):
        with open('wiki20.csv', 'a') as file:
            writer = csv.writer(file, delimiter=' ')
            writer.writerow((data['name'], data['birthday']))

    def write_csvElse(self, data):
        with open('wikiElse.csv', 'a') as file:
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
        # if wiki_pages[1].text.find("Следующая страница (Фабер, Даниэль Тобиас)"):
        if wiki_pages[1].text.find('Следующая страница (ФК "Спартак" Москва в сезоне 1968)'):
            page = 'https://ru.wikipedia.org' + wiki_pages[1].get('href')
            pages.append(page)
            self.get_All_Links_On_Wiki(self.get_Html(page), pages)
        else:
            print("End. Pages were visited: " + str(len(pages)))

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

    def main(self):
        url = 'https://ru.wikipedia.org/wiki/%D0%A1%D0%BB%D1%83%D0%B6%D0%B5%D0%B1%D0%BD%D0%B0%D1%8F:%D0%92%D1%81%D0%B5_%D1%81%D1%82%D1%80%D0%B0%D0%BD%D0%B8%D1%86%D1%8B/%D0%A4'
        wiki_pages = []
        wiki_pages.append(url)
        self.get_All_Links_On_Wiki(self.get_Html(url), wiki_pages)
        for pages in wiki_pages:
            link = self.get_All_Links_On_Page(self.get_Html(pages))
            for i in link:
                html = self.get_Html(i)
                self.get_Page_Data(html)


# main
wiki = Wiki()
start_time = time()
wiki.main()
print("Program's end")
end_time = time()
time_program = end_time - start_time
file = open("Program's time.txt", 'w')
file.write(str(time_program))
file.close()
