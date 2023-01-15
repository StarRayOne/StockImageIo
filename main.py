import time
import csv
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from seleniumwire import webdriver
import os
from bs4 import BeautifulSoup
import lxml
from playwright.sync_api import Playwright, sync_playwright, expect
import asyncio
from multiprocessing import Process
import get_links

# Служебная инфа
fake_head = {
    "user-agent": 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'}
all_links = []
proxy_play = {
    "server": "http://185.202.2.152:8000",
    "username": "bQ7pdR",
    "password": "EyJGTv"
}
proxy_req = {
    'http': 'http://bQ7pdR:EyJGTv@185.202.2.152:8000'
}

# чтение ссылок и создание файлов
section = input('Введите название категории из которой будем качать фото (ссылки должны быть в папке): ')
with open(f'{section}/links_{section}.csv', 'r', newline='') as file:
    reader = csv.DictReader(file, delimiter=';')
    for row in reader:
        all_links.append(row['link'])
    print(f'Будем скачивать: {len(all_links)} фото')

n = len(all_links) // 5
print(f'Будем брать по {n} фото на поток')
with open(f'{section}/info.csv', 'w', newline='') as file:
    writer = csv.writer(file, delimiter=';')
    writer.writerow(['number', 'link', 'name', 'tags', 'resolution'])
with open(f'{section}/logs.csv', 'w', newline='') as file:
    writer = csv.writer(file, delimiter=';')
    writer.writerow(['number', 'link'])
input('НАЧИНАЕМ? ')
print('Погнали!')
start_time = time.time()


# ЗАПИСЫВАЕМ COUNT НАЧИНАЯ СО ВТОРОГО ПОТОКА ТАКЖЕ КАК И НУЖНОЕ ЧИСЛО В ТАБЛИЦЕ, НО НАЧИНАЕМ СРЕЗ all_links[count-1:до нужного значения]
def multi_downloads():
    start_time = time.time()

    def download1():
        count = 1
        for link in all_links[:n]:
            def run(playwright: Playwright) -> None:
                browser1 = playwright.chromium.launch(headless=False)
                context1 = browser1.new_context()
                page = context1.new_page()
                try:
                    page.goto(link, timeout=100)
                except:
                    try:

                        # функция скачивания
                        with page.expect_download() as download_info:
                            page.get_by_role("button", name="Free Download").click()
                        download = download_info.value
                        download.save_as(f'{section}/main_{section}/{section}_{count}.jpg')
                        # функция парсинга страницы
                        htmlcode = page.inner_html('html')
                        soup = BeautifulSoup(htmlcode, 'lxml')
                        preview = soup.find('figure', itemprop="image").find('img')['src']
                        download_preview = requests.get(url=preview, stream=True, headers=fake_head)
                        with open(f'{section}/preview_{section}/preview_{section}_{count}.jpg', 'wb') as prew:
                            prew.write(download_preview.content)
                        name = soup.find('h1').find('span').text.replace(' Free Stock Image', '')
                        tags = [tag.text for tag in
                                soup.find(class_="photo-tags").find(itemprop='keywords').find_all('a')]
                        resolution = \
                            [res.find('span').text for res in soup.find(class_="stats clearfix").find_all('li')][4]
                        with open(f'{section}/info.csv', 'a', newline='') as file:
                            writer = csv.writer(file, delimiter=';')
                            writer.writerow([count, link, name, tags, resolution])
                    except:
                        with open(f'{section}/logs.csv', 'a', newline='') as file:
                            writer = csv.writer(file, delimiter=';')
                            writer.writerow([count, link])

                # ---------------------
                context1.close()
                browser1.close()

            with sync_playwright() as playwright:
                run(playwright)
            count += 1
        print('Скачивание потока 1 закончили!')
        print("--- %s секунд ---" % (time.time() - start_time))

    def download2():
        count = n
        for link in all_links[n - 1:n * 2]:
            def run(playwright: Playwright) -> None:
                browser1 = playwright.chromium.launch(headless=False)
                context1 = browser1.new_context()
                page = context1.new_page()
                try:
                    page.goto(link, timeout=100)
                except:
                    try:

                        # функция скачивания
                        with page.expect_download() as download_info:
                            page.get_by_role("button", name="Free Download").click()
                        download = download_info.value
                        download.save_as(f'{section}/main_{section}/{section}_{count}.jpg')
                        # функция парсинга страницы
                        htmlcode = page.inner_html('html')
                        soup = BeautifulSoup(htmlcode, 'lxml')
                        preview = soup.find('figure', itemprop="image").find('img')['src']
                        download_preview = requests.get(url=preview, stream=True, headers=fake_head)
                        with open(f'{section}/preview_{section}/preview_{section}_{count}.jpg', 'wb') as prew:
                            prew.write(download_preview.content)
                        name = soup.find('h1').find('span').text.replace(' Free Stock Image', '')
                        tags = [tag.text for tag in
                                soup.find(class_="photo-tags").find(itemprop='keywords').find_all('a')]
                        resolution = \
                            [res.find('span').text for res in soup.find(class_="stats clearfix").find_all('li')][4]
                        with open(f'{section}/info.csv', 'a', newline='') as file:
                            writer = csv.writer(file, delimiter=';')
                            writer.writerow([count, link, name, tags, resolution])
                    except:
                        with open(f'{section}/logs.csv', 'a', newline='') as file:
                            writer = csv.writer(file, delimiter=';')
                            writer.writerow([count, link])

                # ---------------------
                context1.close()
                browser1.close()

            with sync_playwright() as playwright:
                run(playwright)
            count += 1
        print('Скачивание потока 2 закончили!')
        print("--- %s секунд ---" % (time.time() - start_time))

    def download3():
        count = n * 2
        for link in all_links[n * 2 - 1:n * 3]:
            def run(playwright: Playwright) -> None:
                browser1 = playwright.chromium.launch(headless=False)
                context1 = browser1.new_context()
                page = context1.new_page()
                try:
                    page.goto(link, timeout=100)
                except:
                    try:

                        # функция скачивания
                        with page.expect_download() as download_info:
                            page.get_by_role("button", name="Free Download").click()
                        download = download_info.value
                        download.save_as(f'{section}/main_{section}/{section}_{count}.jpg')
                        # функция парсинга страницы
                        htmlcode = page.inner_html('html')
                        soup = BeautifulSoup(htmlcode, 'lxml')
                        preview = soup.find('figure', itemprop="image").find('img')['src']
                        download_preview = requests.get(url=preview, stream=True, headers=fake_head)
                        with open(f'{section}/preview_{section}/preview_{section}_{count}.jpg', 'wb') as prew:
                            prew.write(download_preview.content)
                        name = soup.find('h1').find('span').text.replace(' Free Stock Image', '')
                        tags = [tag.text for tag in
                                soup.find(class_="photo-tags").find(itemprop='keywords').find_all('a')]
                        resolution = \
                            [res.find('span').text for res in soup.find(class_="stats clearfix").find_all('li')][4]
                        with open(f'{section}/info.csv', 'a', newline='') as file:
                            writer = csv.writer(file, delimiter=';')
                            writer.writerow([count, link, name, tags, resolution])
                    except:
                        with open(f'{section}/logs.csv', 'a', newline='') as file:
                            writer = csv.writer(file, delimiter=';')
                            writer.writerow([count, link])

                # ---------------------
                context1.close()
                browser1.close()

            with sync_playwright() as playwright:
                run(playwright)
            count += 1
        print('Скачивание потока 3 закончили!')
        print("--- %s секунд ---" % (time.time() - start_time))

    def download4():
        count = n * 3
        for link in all_links[n * 3 - 1: n * 4]:
            def run(playwright: Playwright) -> None:
                browser1 = playwright.chromium.launch(headless=False)
                context1 = browser1.new_context()
                page = context1.new_page()
                try:
                    page.goto(link, timeout=100)
                except:
                    try:

                        # функция скачивания
                        with page.expect_download() as download_info:
                            page.get_by_role("button", name="Free Download").click()
                        download = download_info.value
                        download.save_as(f'{section}/main_{section}/{section}_{count}.jpg')
                        # функция парсинга страницы
                        htmlcode = page.inner_html('html')
                        soup = BeautifulSoup(htmlcode, 'lxml')
                        preview = soup.find('figure', itemprop="image").find('img')['src']
                        download_preview = requests.get(url=preview, stream=True, headers=fake_head)
                        with open(f'{section}/preview_{section}/preview_{section}_{count}.jpg', 'wb') as prew:
                            prew.write(download_preview.content)
                        name = soup.find('h1').find('span').text.replace(' Free Stock Image', '')
                        tags = [tag.text for tag in
                                soup.find(class_="photo-tags").find(itemprop='keywords').find_all('a')]
                        resolution = \
                            [res.find('span').text for res in soup.find(class_="stats clearfix").find_all('li')][4]
                        with open(f'{section}/info.csv', 'a', newline='') as file:
                            writer = csv.writer(file, delimiter=';')
                            writer.writerow([count, link, name, tags, resolution])
                    except:
                        with open(f'{section}/logs.csv', 'a', newline='') as file:
                            writer = csv.writer(file, delimiter=';')
                            writer.writerow([count, link])

                # ---------------------
                context1.close()
                browser1.close()

            with sync_playwright() as playwright:
                run(playwright)
            count += 1
        print('Скачивание потока 4 закончили!')
        print("--- %s секунд ---" % (time.time() - start_time))

    def download5():
        count = n * 4
        for link in all_links[n * 4 - 1: n * 5]:
            def run(playwright: Playwright) -> None:
                browser1 = playwright.chromium.launch(headless=False)
                context1 = browser1.new_context()
                page = context1.new_page()
                try:
                    page.goto(link, timeout=100)
                except:
                    try:
                        # функция скачивания
                        with page.expect_download() as download_info:
                            page.get_by_role("button", name="Free Download").click()
                        download = download_info.value
                        download.save_as(f'{section}/main_{section}/{section}_{count}.jpg')
                        # функция парсинга страницы
                        htmlcode = page.inner_html('html')
                        soup = BeautifulSoup(htmlcode, 'lxml')
                        preview = soup.find('figure', itemprop="image").find('img')['src']
                        download_preview = requests.get(url=preview, stream=True, headers=fake_head)
                        with open(f'{section}/preview_{section}/preview_{section}_{count}.jpg', 'wb') as prew:
                            prew.write(download_preview.content)
                        name = soup.find('h1').find('span').text.replace(' Free Stock Image', '')
                        tags = [tag.text for tag in
                                soup.find(class_="photo-tags").find(itemprop='keywords').find_all('a')]
                        resolution = \
                            [res.find('span').text for res in soup.find(class_="stats clearfix").find_all('li')][4]
                        with open(f'{section}/info.csv', 'a', newline='') as file:
                            writer = csv.writer(file, delimiter=';')
                            writer.writerow([count, link, name, tags, resolution])
                    except:
                        with open(f'{section}/logs.csv', 'a', newline='') as file:
                            writer = csv.writer(file, delimiter=';')
                            writer.writerow([count, link])

                # ---------------------
                context1.close()
                browser1.close()

            with sync_playwright() as playwright:
                run(playwright)
            count += 1
        print('Скачивание потока 5 закончили!')
        print("--- %s секунд ---" % (time.time() - start_time))
    def download6():
        count = n * 5
        for link in all_links[n * 5 - 1:]:
            def run(playwright: Playwright) -> None:
                browser1 = playwright.chromium.launch(headless=False, proxy=proxy_play)
                context1 = browser1.new_context()
                page = context1.new_page()
                try:
                    page.goto(link, timeout=100)
                except:
                    try:
                        # функция скачивания
                        with page.expect_download() as download_info:
                            page.get_by_role("button", name="Free Download").click()
                        download = download_info.value
                        download.save_as(f'{section}/main_{section}/{section}_{count}.jpg')
                        # функция парсинга страницы
                        htmlcode = page.inner_html('html')
                        soup = BeautifulSoup(htmlcode, 'lxml')
                        preview = soup.find('figure', itemprop="image").find('img')['src']
                        download_preview = requests.get(url=preview, stream=True, headers=fake_head, proxies=proxy_req)
                        with open(f'{section}/preview_{section}/preview_{section}_{count}.jpg', 'wb') as prew:
                            prew.write(download_preview.content)
                        name = soup.find('h1').find('span').text.replace(' Free Stock Image', '')
                        tags = [tag.text for tag in
                                soup.find(class_="photo-tags").find(itemprop='keywords').find_all('a')]
                        resolution = \
                            [res.find('span').text for res in soup.find(class_="stats clearfix").find_all('li')][4]
                        with open(f'{section}/info.csv', 'a', newline='') as file:
                            writer = csv.writer(file, delimiter=';')
                            writer.writerow([count, link, name, tags, resolution])
                    except:
                        with open(f'{section}/logs.csv', 'a', newline='') as file:
                            writer = csv.writer(file, delimiter=';')
                            writer.writerow([count, link])

                # ---------------------
                context1.close()
                browser1.close()

            with sync_playwright() as playwright:
                run(playwright)
            count += 1
        print('Скачивание потока 6 закончили!')
        print("--- %s секунд ---" % (time.time() - start_time))

    Process(target=download1).start()
    Process(target=download2).start()
    Process(target=download3).start()
    Process(target=download4).start()
    Process(target=download5).start()
    Process(target=download6).start()



multi_downloads()
