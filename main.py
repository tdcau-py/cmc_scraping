import os
import csv
import requests

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def header():
    return {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0'
    }


def get_html(url: str):
    """Возвращает html-страницу"""
    headers = header()
    req = requests.get(url, headers=headers)

    if req.text:
        return req.text

    return False


def get_links_to_item_source(domen: str, index_html: str) -> list:
    """Собирает ссылки на все ресурсы"""
    links_to_src = []

    # with open(f'data/index.html', 'r', encoding='utf-8') as file:
    #     html_cmc = file.read()

    bs = BeautifulSoup(index_html, 'lxml')
    table_trs = bs.find(class_='cmc-table').find('tbody').find_all('tr')

    for tr in table_trs:
        url_link = domen + tr.find(class_='cmc-link')['href']
        links_to_src.append(url_link)

    return links_to_src


def writing_data_to_csv(num_data: int, title: str, data: dict):
    """Записывает полученные данные в CSV файл"""
    dir_result = os.path.join(os.getcwd(), 'result')
    csv_file_name = 'cmc_data.csv'
    path_to_csv_file = os.path.join(dir_result, csv_file_name)

    titles = ['№', 'Title', 'Websites', 'Socials', 'Chat']
    websites = '\n'.join(data['Sites'])
    socials = '\n'.join(data['Community'])
    chat = '\n'.join(data['Chat'])

    if not os.path.exists(dir_result):
        os.system(f'mkdir {dir_result}')
        print('Создана папка "result"...')

    if not os.path.exists(path_to_csv_file):
        with open(path_to_csv_file, 'w', encoding='utf-8', newline='') as csv_file:
            csvwriter = csv.DictWriter(csv_file, fieldnames=titles, dialect='excel')
            csvwriter.writeheader()

            print(f'Создан файл {csv_file_name}...')

            csvwriter.writerow({
                '№': num_data,
                'Title': title, 
                'Websites': websites,
                'Socials': socials, 
                'Chat': chat,
                })

    else:
        with open(path_to_csv_file, 'a', encoding='utf-8', newline='') as csv_file:
            csvwriter = csv.DictWriter(csv_file, fieldnames=titles, dialect='excel')
            csvwriter.writerow({
                '№': num_data,
                'Title': title, 
                'Websites': websites,
                'Socials': socials, 
                'Chat': chat,
                })

    print('Данные записаны... Переход к следующему ресурсу...\n')


def main(src_url: str, count_operation: int):
    """Получение данных"""
    src_name = src_url.split('/')[-2]

    chrome_options = Options()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(
        executable_path='chromedriver/chromedriver.exe',
        options=chrome_options,
    )
    
    driver.get(src_url)
    driver.minimize_window()
    page_source = driver.page_source
    
    with open(f'data/page_{src_name}.html', 'w', encoding='utf-8') as file:
        file.write(page_source)

    print(f'Выгружен html-код страницы ресурса {count_operation}...')

    with open(f'data/page_{src_name}.html', 'r', encoding='utf-8') as file:
        html = file.read()

    bs = BeautifulSoup(html, 'lxml')
    title = bs.find(class_='fLa-dNu').text

    print(f'Обработка страницы {title}')

    content_links = bs.find(class_='jfPVkR').find(class_='jfPVkR').find_all(class_='geHuRS')
    
    sites = []
    chats = []
    communities = []
    data = {}

    for content in content_links:
        section_name = content.find('h6').text

        if section_name == 'Links':
            links = content.find_all('a')

            for link in links:
                if link.text.strip() not in ('Whitepaper', 'Source code'):
                    if link.text.strip() == 'Chat':
                        if link['href'].startswith('https://t.me') or link['href'].startswith('https://discord.gg'):
                            chats.append(link['href'])

                    else:
                        sites.append(link['href'])

        elif section_name == 'Community':
            
            links = content.find_all('a')

            for link in links:
                if link.text.strip() == 'Twitter' or link.text.strip() == 'Reddit':
                    communities.append(link['href'])
            
    data['Sites'] = sites
    data['Community'] = communities
    data['Chat'] = chats

    writing_data_to_csv(count_operation, title, data)
    
    return data


if __name__ == '__main__':
    cmc_domen = 'https://coinmarketcap.com'
    print('Начало парсинга...')

    count = 0

    for num_page in range(1, 92):
        cmc_page_url = f'{cmc_domen}/?page={num_page}'

        print(f'\nСтраница {num_page}.')

        html_code = get_html(cmc_page_url)

        if html_code:
            if not os.path.exists(os.path.join(os.getcwd(), 'data')):
                os.system('mkdir data')
                print('Создана папка "data".\n')

            with open(f'data/index_{num_page}.html', 'w', encoding='utf-8') as file:
                file.write(html_code)

            print('Создан файл с html-кодом главной страницы.')

            with open(f'data/index_{num_page}.html', 'r', encoding='utf-8') as file:
                main_html = file.read()

            links_to_coins = get_links_to_item_source(cmc_domen, main_html)

            for link in links_to_coins:
                count += 1

                print(f'Парсинг ресурса по ссылке {link}...\n')

                if link.split('/')[-2] == 'vechain':
                    continue

                main(link, count)

    print('\nПарсинг завершен.')
