import json

from bs4 import BeautifulSoup
import requests
import csv


class ParseHtml:
    def __init__(self, url: str):
        self.url = url

    @property
    def header(self):
        return {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 YaBrowser/23.3.1.806 Yowser/2.5 Safari/537.36'
        }

    def get_html(self):
        """Возвращает html-страницу"""
        req = requests.get(self.url, headers=self.header)

        if req.text:
            return req.text

        return False


class Sensors:
    def __init__(self):
        self.url = 'https://sensors.saasexch.com/sa.gif?project=cmc'

    @property
    def header(self):
        return {
            'accept': '*/*',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 YaBrowser/23.3.1.806 Yowser/2.5 Safari/537.36'
        }

    def get_data(self):
        req = requests.post(self.url, headers=self.header)

        if req.text:
            return req.text

        return False


if __name__ == '__main__':
    cmc_domen = 'https://coinmarketcap.com'
    cmc_url = 'https://coinmarketcap.com/?page=1'

    cmc_main = ParseHtml(cmc_url)
    html_code = cmc_main.get_html()

    if html_code:
        # with open('index.html', 'w', encoding='utf-8') as file:
        #     file.write(html_code)

        with open('index.html', 'r', encoding='utf-8') as file:
            html_cmc = file.read()

        # Сбор ссылок на ресурсы
        bs = BeautifulSoup(html_cmc, 'lxml')
        cmc_links = bs.find('table').find_all('a', class_='cmc-link')

        links_to_src = []

        for link in cmc_links:
            url_link = cmc_domen + link['href']
            links_to_src.append(url_link)

        count = 0

        for link in links_to_src:
            if count == 0:
                src_page = ParseHtml(link)
                html_src = src_page.get_html()

                bs_link = BeautifulSoup(html_src, 'lxml')
                src_div = bs_link.find(class_='nameSection')

                src_title = src_div.find(class_='sc-1d5226ca-0')

                print(src_title.text)

            count += 1
