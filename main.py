import time

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

service = Service()

options = webdriver.ChromeOptions()

driver = webdriver.Chrome(service=service, options=options)

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

time.sleep(3)

# elements_titles = driver.find_elements(By.CLASS_NAME,'PagePromo-title')[6:]
# elements_img = driver.find_elements(By.XPATH,'//img[@class="Image"]')[2:]
#screenshot_as_base64

# news_elements = driver.find_elements(By.CLASS_NAME,'PageList-items-item')[6:]
news_elements = driver.find_elements(By.CLASS_NAME,'PagePromo-content')



print('')
