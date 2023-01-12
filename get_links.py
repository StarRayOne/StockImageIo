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
def get_images():
    with webdriver.Chrome() as browser:
        actions = ActionChains(browser)
        browser.get('https://stocksnap.io/search/business')
        time.sleep(1)
        browser.execute_script("window.stop();")
        while True:
            try:
                load = browser.find_element(By.CLASS_NAME, 'load-more-photos')
                actions.move_to_element(load).perform()
                time.sleep(1)
                browser.execute_script("window.stop();")
                browser.refresh()
            except:
                page = browser.page_source
                soup = BeautifulSoup(page, 'lxml')
                links = [f'https://stocksnap.io{link["href"]}' for link in soup.find_all(class_='photo-grid-preview')]
                all_links.extend(links)
                break

get_images()
with open('links.csv', 'w', newline='') as file:
    writer = csv.writer(file, delimiter=',')
    writer.writerow(['link'])
    for link in all_links:
        writer.writerow([link])