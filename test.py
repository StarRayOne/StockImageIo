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
        from playwright.sync_api import Playwright, sync_playwright, expect

        def run(playwright: Playwright) -> None:
            browser = playwright.chromium.launch(headless=False)
            context = browser.new_context()
            page = context.new_page()
            page.goto("https://stocksnap.io/search/beach")

            # ---------------------
            context.close()
            browser.close()

        with sync_playwright() as playwright:
            run(playwright)


download1()
