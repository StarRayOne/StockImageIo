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

all_links = []
start_time = time.time()

with open('links_dogs.csv', 'r', newline='') as file:
    reader = csv.DictReader(file, delimiter=';')
    for row in reader:
        all_links.append(row['link'])
    print(all_links)
    print(f'{len(all_links)}')

with open('logs.csv', 'w', newline='') as file:
    writer = csv.writer(file, delimiter=';')
    writer.writerow(['number', 'link'])


# ЗАПИСЫВАЕМ COUNT НАЧИНАЯ СО ВТОРОГО ПОТОКА ТАКЖЕ КАК И НУЖНОЕ ЧИСЛО В ТАБЛИЦЕ, НО НАЧИНАЕМ СРЕЗ all_links[count-1:до нужного значения]
def multi_downloads():
    start_time = time.time()

    def download1():
        count = 1
        for link in all_links[:100]:
            def run(playwright: Playwright) -> None:
                browser1 = playwright.chromium.launch(headless=False)
                context1 = browser1.new_context()
                page = context1.new_page()
                try:
                    page.goto(link, timeout=3000)
                    with page.expect_download() as download_info:
                        page.get_by_role("button", name="Free Download").click()
                    download = download_info.value
                    download.save_as(f'/home/hack/Загрузки/dog{count}.jpg')
                except:
                    try:
                        # функция парсинга страницы
                        htmlcode = page.inner_html('html')
                        soup = BeautifulSoup(htmlcode, 'lxml')
                        tags = [tag.text for tag in soup.find(class_="photo-tags").find_all('a')]
                        resolution = \
                        [res.find('span').text for res in soup.find(class_="stats clearfix").find('ul').find_all('li')][
                            4]
                        # функция скачивания
                        with page.expect_download() as download_info:
                            page.get_by_role("button", name="Free Download").click()
                        download = download_info.value
                        download.save_as(f'/home/hack/Загрузки/dog{count}.jpg')
                    except:
                        with open('logs.csv', 'a', newline='') as file:
                            writer = csv.writer(file, delimiter=';')
                            writer.writerow([count, link])
                # ---------------------
                context1.close()
                browser1.close()

            with sync_playwright() as playwright:
                run(playwright)
            count += 1
            print(f'Поток 1 Скачали фото {count}')
        print('Скачивание потока 1 закончили!')
        print("--- %s секунд ---" % (time.time() - start_time))

    def download2():
        count = 100
        for link in all_links[99:200]:
            def run(playwright: Playwright) -> None:
                browser = playwright.chromium.launch(headless=False)
                context = browser.new_context()
                page = context.new_page()
                try:
                    page.goto(link, timeout=3000)
                    with page.expect_download() as download_info:
                        page.get_by_role("button", name="Free Download").click()
                    download = download_info.value
                    download.save_as(f'/home/hack/Загрузки/dog{count}.jpg')
                except:
                    try:
                        with page.expect_download() as download_info:
                            page.get_by_role("button", name="Free Download").click()
                        download = download_info.value
                        download.save_as(f'/home/hack/Загрузки/dog{count}.jpg')
                    except:
                        with open('logs.csv', 'a', newline='') as file:
                            writer = csv.writer(file, delimiter=';')
                            writer.writerow([count, link])
                context.close()
                browser.close()

            with sync_playwright() as playwright:
                run(playwright)
            count += 1
            print(f'Поток 2 Скачали фото {count}')
        print('Скачивание потока 2 закончили!')
        print("--- %s секунд ---" % (time.time() - start_time))

    def download3():
        count = 200
        for link in all_links[190:300]:
            def run(playwright: Playwright) -> None:
                browser = playwright.chromium.launch(headless=False)
                context = browser.new_context()
                page = context.new_page()
                try:
                    page.goto(link, timeout=3000)
                    with page.expect_download() as download_info:
                        page.get_by_role("button", name="Free Download").click()
                    download = download_info.value
                    download.save_as(f'/home/hack/Загрузки/dog{count}.jpg')
                except:
                    try:
                        with page.expect_download() as download_info:
                            page.get_by_role("button", name="Free Download").click()
                        download = download_info.value
                        download.save_as(f'/home/hack/Загрузки/dog{count}.jpg')
                    except:
                        with open('logs.csv', 'a', newline='') as file:
                            writer = csv.writer(file, delimiter=';')
                            writer.writerow([count, link])
                context.close()
                browser.close()

            with sync_playwright() as playwright:
                run(playwright)
            count += 1
            print(f'Поток 3 Скачали фото {count}')
        print('Скачивание потока 3 закончили!')
        print("--- %s секунд ---" % (time.time() - start_time))

    def download4():
        count = 300
        for link in all_links[299:400]:
            def run(playwright: Playwright) -> None:
                browser = playwright.chromium.launch(headless=False)
                context = browser.new_context()
                page = context.new_page()
                try:
                    page.goto(link, timeout=3000)
                    with page.expect_download() as download_info:
                        page.get_by_role("button", name="Free Download").click()
                    download = download_info.value
                    download.save_as(f'/home/hack/Загрузки/dog{count}.jpg')
                except:
                    try:
                        with page.expect_download() as download_info:
                            page.get_by_role("button", name="Free Download").click()
                        download = download_info.value
                        download.save_as(f'/home/hack/Загрузки/dog{count}.jpg')
                    except:
                        with open('logs.csv', 'a', newline='') as file:
                            writer = csv.writer(file, delimiter=';')
                            writer.writerow([count, link])

                context.close()
                browser.close()

            with sync_playwright() as playwright:
                run(playwright)
            count += 1
            print(f'Поток 4 Скачали фото {count}')
        print('Скачивание потока 4 закончили!')
        print("--- %s секунд ---" % (time.time() - start_time))

    def download5():
        count = 400
        for link in all_links[399:]:
            def run(playwright: Playwright) -> None:
                browser = playwright.chromium.launch(headless=False)
                context = browser.new_context()
                page = context.new_page()
                try:
                    page.goto(link, timeout=3000)
                    with page.expect_download() as download_info:
                        page.get_by_role("button", name="Free Download").click()
                    download = download_info.value
                    download.save_as(f'/home/hack/Загрузки/dog{count}.jpg')
                except:
                    try:
                        with page.expect_download() as download_info:
                            page.get_by_role("button", name="Free Download").click()
                        download = download_info.value
                        download.save_as(f'/home/hack/Загрузки/dog{count}.jpg')
                    except:
                        with open('logs.csv', 'a', newline='') as file:
                            writer = csv.writer(file, delimiter=';')
                            writer.writerow([count, link])
                context.close()
                browser.close()

            with sync_playwright() as playwright:
                run(playwright)
            count += 1
            print(f'Поток 5 Скачали фото {count}')
        print('Скачивание потока 5 закончили!')
        print("--- %s секунд ---" % (time.time() - start_time))

    Process(target=download1).start()
    Process(target=download2).start()
    Process(target=download3).start()
    Process(target=download4).start()
    Process(target=download5).start()


multi_downloads()
print('Все загрузки закончили!')
print("--- %s секунд ---" % (time.time() - start_time))
