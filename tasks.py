import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
import re
import base64 as b64
from robocorp.tasks import task


# Logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@task
def main(phrases):
    
    # Initialize the Chrome driver service
    service = Service()

    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')  # Uncomment for headless mode
    driver = webdriver.Chrome(service=service, options=options)

    logging.info('Starting Browser')

    # Website URL
    url = 'https://apnews.com/'
    count = 1
    for phrase in phrases:
        # Open browser
        driver.get(url)
        driver.maximize_window()

        # Setting wait conditions
        wait = WebDriverWait(driver, 10)
        logging.info(f'Searching for phrase: {phrase}')

        # Begin search
        wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'SearchOverlay-search-button'))).click()
        wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'SearchOverlay-search-input'))).send_keys(phrase)
        driver.find_element(By.CLASS_NAME, 'SearchOverlay-search-input').submit()

        drop_SortBy = driver.find_element(By.CLASS_NAME, 'Select-input')
        Select(drop_SortBy).select_by_visible_text('Newest')
        driver.refresh()

        wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'SearchResultsModule-results')))
        time.sleep(5)  # Adjust sleep time if necessary
        news_elements = driver.find_elements(By.CLASS_NAME, 'SearchResultsModule-results')
        news_elements = news_elements[0].find_elements(By.CLASS_NAME, 'PageList-items-item')

        for item in news_elements:
            try:
                title_element = item.find_element(By.CLASS_NAME, 'PagePromoContentIcons-text').text
                date_element = item.find_element(By.CLASS_NAME, 'PagePromo-date').text
                description_element = item.find_element(By.CLASS_NAME, 'PagePromo-description').text
                Titles.append(title_element)
                Descriptions.append(description_element)
                Dates.append(date_element)
                imgs.append(f'{outputFolder}/image{count}.jpeg')
                moneys.append(hasMoney(title_element + description_element))
            except Exception as e:
                logging.error(f'Error processing item {count}: {e}')

            try:
                img_element = item.find_element(By.CLASS_NAME, 'PagePromo-media').screenshot_as_base64

            except:
                img_element = None

            # Decoding the image and writing it
            imageFile = f'{outputFolder}/image{count}.jpeg'
            b64ToImage(imageFile, img_element)
            count = count + 1

    logging.info('All news has been captured!')
    driver.quit()  # Close the browser


def b64ToImage(path, content):
    if content is None:
        return
    content = b64.b64decode(content)
    with open(path, 'wb') as file:
        file.write(content)


def hasMoney(string):
    return bool(re.search(r'(\$[0-9,]+(\.\d{2})?)|(USD|dollars)', string))


Titles = []
Descriptions = []
Dates = []
imgs = []
moneys = []

outputFolder = './Output'
os.makedirs(outputFolder, exist_ok=True)

# List of phrases to be searched
phrases = ['economy', 'politics', 'technology']


main(phrases)

data = {
    'Title': Titles,
    'Date': Dates,
    'Description': Descriptions,
    'Picture': imgs,
    'Contains Money?': moneys
}

# Create a dataframe
df = pd.DataFrame(data)
df.to_excel(f'./{outputFolder}/output.xlsx', index=False)
