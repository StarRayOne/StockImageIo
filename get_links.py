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
import os

all_links = []
section = input('Введите название категории из которой будем парсить ссылки: ')
os.mkdir(f'{section}')
os.mkdir(f'{section}/main_{section}')
os.mkdir(f'{section}/preview_{section}')

def get_images():
    with webdriver.Chrome() as browser:
        actions = ActionChains(browser)
        browser.get(f'https://stocksnap.io/search/{section}')
        time.sleep(1)
        while True:
            try:
                load = browser.find_element(By.CLASS_NAME, 'load-more-photos')
                actions.move_to_element(load).perform()
                browser.refresh()
                time.sleep(3)
            except:
                time.sleep(3)
                page = browser.page_source
                soup = BeautifulSoup(page, 'lxml')
                links = [f'https://stocksnap.io{link["href"]}' for link in soup.find_all(class_='photo-grid-preview')]
                all_links.extend(links)
                break


get_images()
with open(f'{section}/links_{section}.csv', 'w', newline='') as file:
    writer = csv.writer(file, delimiter=';')
    writer.writerow(['link'])
    for link in all_links:
        writer.writerow([link])
    print(f'Сохранили {len(all_links)} ссылок!')
