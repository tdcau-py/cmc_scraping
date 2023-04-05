import json
import time

from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

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
    def __init__(self, url):
        self.url = url

    @property
    def header(self):
        return {
            'Referer': 'https://s2.coinmarketcap.com/',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 YaBrowser/23.3.1.806 Yowser/2.5 Safari/537.36'
        }

    def get_data(self):
        req = requests.post(self.url, headers=self.header)

        if req.text:
            return req.text

        return False
    

def get_dynamic_data(url):
    chrome_options = Options()
    chrome_options.add_argument('--headless')

    driver = webdriver.Chrome(
        executable_path='chromedriver/chromedriver',
        options=chrome_options,
    )

    driver.get(url=url)
    time.sleep(3)

    print(driver.find_element(By.CLASS_NAME, 'dropdownItem').text)

    return driver.close()


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
        cmc_table_tr = bs.find(class_='cmc-table').find('tbody').find_all('tr')

        links_to_src = []

        for tr in cmc_table_tr:
            link = tr.find('a', class_='cmc-link')
            url_link = cmc_domen + link['href']
            links_to_src.append(url_link)

        count = 0

        for link in links_to_src:
            if count == 2:
                break
            else:
                src_page = ParseHtml(link)
                html_src = src_page.get_html()

                # with open(f'data/{count}_link.html', 'w', encoding='utf-8') as file:
                #     file.write(html_src)

                bs_link = BeautifulSoup(html_src, 'lxml')
                
                src_name_header = bs_link.find(class_='nameSection').find(class_='nameHeader')

                src_title = src_name_header.find(class_='sc-1d5226ca-0').text

                # src_links_section = bs_link.find(class_='linksSection').find(class_='content').find_all('li')

                get_dynamic_data(link)

                


            count += 1
