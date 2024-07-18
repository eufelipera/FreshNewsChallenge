import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import logging
import re
import base64 as b64

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

    wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'SearchResultsModule-results')))
    time.sleep(5)
    news_elements = driver.find_elements(By.CLASS_NAME,'SearchResultsModule-results')
    news_elements = news_elements[0].find_elements(By.CLASS_NAME,'PageList-items-item')

    for count, item in enumerate(news_elements):
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
        imgs.append(f'{outputFolder}/image{count}.jpeg')
        moneys.append(hasMoney(Title_element + description_element))

        #decoding the image and writing it
        b64ToImage(f'./{outputFolder}/image{count}.jpeg',img_element)
    logging.info('All news has been captured!')

def b64ToImage(path,content):
    if content == None:
        return
    content = b64.b64decode(content)
    with open(path,'wb') as file:
        file.write(content)

def hasMoney(string):
    return bool(re.search(r'(\$[0-9,]+(\.\d{2})?)|(USD|dollars)', string))

Titles = []
Descriptions = []
Dates = []
imgs = []
moneys = []

outputFolder = './Output'
os.makedirs(outputFolder,exist_ok=True)

main()

data = {
    'Title':Titles,
    'Date':Dates,
    'Description':Descriptions,
    'Picture': imgs,
    'Count phrases':'',
    'Contain Money?':moneys
    }


#create a dataframe
df = pd.DataFrame(data)


df.to_excel(f'./{outputFolder}/output.xlsx', index=False)
