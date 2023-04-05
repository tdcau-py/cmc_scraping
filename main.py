import json
import time

from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

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


def main(src_url: str):
    """Получение данных из динамических элементов"""
    positions = ['Website', 'Community', 'Chat']

    # driver = webdriver.Chrome(
    #     executable_path='chromedriver/chromedriver.exe'
    # )
    #
    # driver.get(src_url)
    # actions = ActionChains(driver)
    # driver.minimize_window()
    #
    # page_source = driver.page_source
    #
    # with open(f'data/page_source.html', 'w', encoding='utf-8') as file:
    #     file.write(page_source)

    with open(f'data/page_source.html', 'r', encoding='utf-8') as file:
        html = file.read()

    bs = BeautifulSoup(html, 'lxml')

    content_links = bs.find_all(class_='geHuRS')

    data = {}
    for content in content_links:
        section_name = content.find('div', class_='fqJtFe').find('h6', class_='modalHeading').text
        print(section_name)

        if section_name in ('Links', 'Community'):
            print('ok')

    # elements = driver.find_elements(By.CSS_SELECTOR, '.geHuRS')
    #
    # data = {}
    # for element in elements:
    #     if element.find_element(By.CLASS_NAME, 'modalHeading').text != 'Explorers':
    #         modal_elements = element.find_elements(By.CLASS_NAME, 'modalLink')
    #
    #         for link in modal_elements:
    #             print(link.get_attribute('href'))
    #
    #         time.sleep(2)

    # elements = driver.find_elements(By.CSS_SELECTOR, '.link-button')

    # data = {}
    # for element in elements:
    #     element_tag = element.tag_name
    #     title = element.find_element(By.CSS_SELECTOR, '.buttonName').text
        
    #     if element_tag == 'a':
    #         if title not in ('Source code', 'Whitepaper', ''):
    #             tooltip_element = element.get_attribute('href')
    #             data[title] = tooltip_element

    #     elif element_tag == 'button':
    #         if title in positions:
    #             actions.move_to_element(element).perform()
    #             tooltip_elements = element.find_element(By.CSS_SELECTOR, '.dropdownItem')

    #             print(tooltip_elements)  
                
                # tooltip_data = {}

                # for item in tooltip_elements:
                #     print(item.text)
                    # if item.text:
                    #     actions.move_to_element(item).perform()
                    #     print(item.text)
                    #     print(item.get_attribute('href'))
                        # link_name = item.text
                        # tooltip_data[link_name] = item.get_attribute('href')

                    # time.sleep(2)

                # data[title] = tooltip_data
            
        # time.sleep(2)

    # driver.close()

    # return data


if __name__ == '__main__':
    cmc_domen = 'https://coinmarketcap.com'
    cmc_url = 'https://coinmarketcap.com/?page=1'

    html_doc = get_html(cmc_url)

    if html_doc:
        # with open('index.html', 'w', encoding='utf-8') as file:
        #     file.write(html_doc)

        links_to_coins = get_links_to_item_source(cmc_domen)

        main(links_to_coins[1])
