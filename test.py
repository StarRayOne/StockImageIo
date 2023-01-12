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
section = 'love'
fake_head = {
    "user-agent": 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'}
all_links = []

with open(f'{section}/links_{section}.csv', 'r', newline='') as file:
    reader = csv.DictReader(file, delimiter=';')
    for row in reader:
        all_links.append(row['link'])
    print(all_links)
    print(f'{len(all_links)}')

with open(f'{section}/info.csv', 'w', newline='') as file:
    writer = csv.writer(file, delimiter=';')
    writer.writerow(['number', 'link', 'name', 'tags', 'resolution'])
with open(f'{section}/logs.csv', 'w', newline='') as file:
    writer = csv.writer(file, delimiter=';')
    writer.writerow(['number', 'link'])


def download1():
    count = 1
    for link in all_links[:50]:
        def run(playwright: Playwright) -> None:
            browser1 = playwright.chromium.launch(headless=False)
            context1 = browser1.new_context()
            page = context1.new_page()
            try:
                page.goto(link, timeout=2500)
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
                    tags = [tag.text for tag in soup.find(class_="photo-tags").find(itemprop='keywords').find_all('a')]
                    resolution = [res.find('span').text for res in soup.find(class_="stats clearfix").find_all('li')][4]
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


download1()
