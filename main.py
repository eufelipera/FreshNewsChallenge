import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

service = Service()

options = webdriver.ChromeOptions()

driver = webdriver.Chrome(service=service, options=options)

#website url
url = 'https://apnews.com/'

#open browser
driver.get(url)
driver.maximize_window()

driver.find_element(By.CLASS_NAME, 'SearchOverlay-search-button').click()
driver.find_element(By.CLASS_NAME, 'SearchOverlay-search-input').send_keys('Trump')
driver.find_element(By.CLASS_NAME, 'SearchOverlay-search-input').submit()

print('')
