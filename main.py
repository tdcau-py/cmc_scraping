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


def main(url_coin_list: str):
    """Получение данных из скрытых элементов"""
    data = {}
    driver = webdriver.Chrome(
        executable_path='chromedriver/chromedriver.exe'
    )

    driver.get(url_coin_list)
    actions = ActionChains(driver)

    title = driver.find_element(By.CLASS_NAME, 'h1').text
    data['title'] = title

    print(data)

    elements = driver.find_elements(By.CSS_SELECTOR, '.link-button')

    sites = []
    for element in elements:
        actions.move_to_element(element).perform()

        if driver.find_element(By.ID, 'tippy-1'):
            sites_element = driver.find_element(By.ID, 'tippy-1').find_elements(By.CLASS_NAME, 'dropdownItem')

            for site in sites_element:
                sites.append(site.get_attribute('href'))

    data['sites'] = sites

    print(data)


if __name__ == '__main__':
    cmc_domen = 'https://coinmarketcap.com'
    cmc_url = 'https://coinmarketcap.com/?page=1'

    html_doc = get_html(cmc_url)

    if html_doc:
        # with open('index.html', 'w', encoding='utf-8') as file:
        #     file.write(html_doc)

        links_to_coins = get_links_to_item_source(cmc_domen)

        main(links_to_coins[1])

        # sites_urls = []
        #
        # for item in tippy_1_block:
        #     sites = item.find_elements(By.CLASS_NAME, 'dropdownItem')
        #
        #     sites_urls = [site.get_attribute('href') for site in sites if site.get_attribute('href')]
        #
        # print(sites_urls)
        # communities = get_sites_data(links_to_coins[1], 'tippy-8')
        #
        # for community in communities:
        #     if community.text == 'twitter':
        #         print(community.text)
