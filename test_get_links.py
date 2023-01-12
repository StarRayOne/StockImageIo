from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://stocksnap.io/search/beach")
    while True:
        try:
            load = browser.find_element(By.CLASS_NAME, 'load-more-photos')
            actions.move_to_element(load).perform()
            browser.refresh()
            time.sleep(1)
        except:
            time.sleep(3)
            page = browser.page_source
            soup = BeautifulSoup(page, 'lxml')
            links = [f'https://stocksnap.io{link["href"]}' for link in soup.find_all(class_='photo-grid-preview')]
            all_links.extend(links)

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
