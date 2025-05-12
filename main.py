import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from lxml import html
import csv

'''
solve captchas as they come
'''

options = uc.ChromeOptions()
options.add_argument("--no-first-run --no-service-autorun --password-store=basic")
options.add_argument("--disable-blink-features=AutomationControlled")

driver = uc.Chrome(options=options)

with open("urls.txt", "r", encoding="utf-8") as f:
    urls = [line.strip() for line in f if line.strip()]

output = []

def get_meta_description_from_google(url):
    query = f"site: {url}"
    search_url = f"https://www.google.com/search?q={query}"
    driver.get(search_url)

    try:
        wait = WebDriverWait(driver, 30)
        wait.until(EC.visibility_of_element_located(
            (By.XPATH, '//div[contains(@style, "-webkit-line-clamp:2")]')
        ))
        if "aren't any great matches for your search" in driver.page_source:
            return "aren't any great matches for your search"
    except:
        if 'did not match any documents' in driver.page_source:
            return 'Your search did not match any documents'

    # Get page source after rendering
    page_source = driver.page_source
    tree = html.fromstring(page_source)

    # Get the first matching element
    element = tree.xpath('//div[@style="-webkit-line-clamp:2"]')
    if element:
        text = element[0].text_content().strip()
        return text
    else:
        print(f"No matching element found for {url}.")

with open('output.csv', 'a', newline='') as file:
    writer = csv.writer(file)
    for url in urls:
        text = get_meta_description_from_google(url)
        writer.writerow([url, text])

driver.quit()
print('all done')