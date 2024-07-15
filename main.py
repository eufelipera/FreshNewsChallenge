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

def main():
    service = Service()

    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')
    driver = webdriver.Chrome(service=service, options=options)

    logging.info('Starting Browser')

    #website url
    url = 'https://apnews.com/'

    #open browser
    driver.get(url)
    driver.maximize_window()

    #setting wait conditions
    wait = WebDriverWait(driver, 5)

    #begin search
    phrase = 'economy'
    wait.until(EC.element_to_be_clickable((By.CLASS_NAME,'SearchOverlay-search-button'))).click()
    wait.until(EC.element_to_be_clickable((By.CLASS_NAME,'SearchOverlay-search-input'))).send_keys(phrase)
    # driver.find_element(By.CLASS_NAME, 'SearchOverlay-search-input').send_keys(phrase)  #searching phrase
    driver.find_element(By.CLASS_NAME, 'SearchOverlay-search-input').submit()


    drop_SortBy = driver.find_element(By.CLASS_NAME, 'Select-input')

    Select(webelement=drop_SortBy).select_by_visible_text('Newest')
    # Select(webelement=drop_SortBy).select_by_visible_text('Oldest')
    driver.refresh()

    Titles = []
    Descriptions = []
    Dates = []
    imgs = []
    moneys = []

    wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'SearchResultsModule-results')))
    time.sleep(3)
    news_elements = driver.find_elements(By.CLASS_NAME,'SearchResultsModule-results')
    news_elements = news_elements[0].find_elements(By.CLASS_NAME,'PageList-items-item')
    for item in news_elements:
        try:

            Title_element = item.find_element(By.CLASS_NAME,'PagePromoContentIcons-text').text
            date_element = item.find_element(By.CLASS_NAME,'PagePromo-date').text
            description_element = item.find_element(By.CLASS_NAME,'PagePromo-description').text
            img_element = item.find_element(By.CLASS_NAME,'PagePromo-media').screenshot_as_base64
        except:
            img_element = None
        Titles.append(Title_element)
        Descriptions.append(description_element)
        Dates.append(date_element)
        imgs.append(img_element)
        moneys.append(hasMoney(Title_element + description_element))
    logging.info('End')

def hasMoney(string):
    return bool(re.search(r'(\$[0-9,]+(\.\d{2})?)|(USD|dollars)', string))


main()
print('End')
