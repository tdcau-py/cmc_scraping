import json

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import requests
import csv


def header():
    return {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 YaBrowser/23.3.1.806 Yowser/2.5 Safari/537.36'
    }


def get_html(url: str):
    """Возвращает html-страницу"""
    headers = header()
    req = requests.get(url, headers=headers)

    if req.text:
        return req.text

    return False


def get_links_to_item_source(domen: str) -> list:
    """Собирает ссылки на все ресурсы"""
    links_to_src = []

    with open('index.html', 'r', encoding='utf-8') as file:
        html_cmc = file.read()

    bs = BeautifulSoup(html_cmc, 'lxml')
    table_trs = bs.find(class_='cmc-table').find('tbody').find_all('tr')

    for tr in table_trs:
        url_link = domen + tr.find(class_='cmc-link')['href']
        links_to_src.append(url_link)

    return links_to_src


def get_sites_data(src_url: str, tippy_attr: str):
    """Получение данных из скрытых элементов"""
    driver = webdriver.Chrome(
        executable_path='chromedriver/chromedriver.exe'
    )

    driver.get(src_url)

    actions = ActionChains(driver)
    element = driver.find_element(By.ID, tippy_attr)
    actions.move_to_element(element).perform()
    tooltip_elements = driver.find_elements(By.CLASS_NAME, 'dropdownItem')

    return tooltip_elements


if __name__ == '__main__':
    cmc_domen = 'https://coinmarketcap.com'
    cmc_url = 'https://coinmarketcap.com/?page=1'

    html_doc = get_html(cmc_url)

    if html_doc:
        # with open('index.html', 'w', encoding='utf-8') as file:
        #     file.write(html_doc)

        links_to_coins = get_links_to_item_source(cmc_domen)

        sites = get_sites_data(links_to_coins[1], '#tippy-1')
        sites_urls = [site.get_attribute('href') for site in sites if site.get_attribute('href')]

        communities = get_sites_data(links_to_coins[1], 'tippy-8')

        for community in communities:
            if community.text == 'twitter':
                print(community.text)
