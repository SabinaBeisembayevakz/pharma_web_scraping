import os
import time
import datetime
import pandas as pd
import random
from bs4 import BeautifulSoup as bs
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
service = Service()
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
browser = webdriver.Chrome(service=service, options=options)




urls_products = []

url = "https://daribar.kz/products?categoryId=148&categoryName=%D0%90%D0%BB%D0%BB%D0%B5%D1%80%D0%B3%D0%B8%D1%8F"
browser.get(url)
# time.sleep(random.randint(0, 10))






# new_html = browser.page_source
# bsobj = bs(new_html, 'html.parser')
# print(bsobj)

# urls=browser.find_elements(By.XPATH,'//*[@id="fbb77615-2bc7-4fe5-81f7-c23f3505ea6e"]/div[2]/div[2]/div[1]/a')
# print(urls)
# for u in urls:
#     url_product=url.get_attribute('href')
#     urls_products.append(url_product)
# print(urls_products)





# # Send an HTTP GET request to the website
# url = "https://daribar.kz/"
# response = requests.get(url)

# # Check if the request was successful (status code 200)
# if response.status_code == 200:
#     # Parse the HTML content of the page using BeautifulSoup
#     soup = BeautifulSoup(response.text, 'html.parser')
#     print(soup)





# ProductCard_link__3PkMj


#     # Example: Let's scrape the titles of articles on the page
#     article_titles = []
#     for article in soup.find_all('article'):
#         title = article.find('h2', class_='entry-title').text.strip()
#         article_titles.append(title)

#     # Print the scraped article titles
#     for i, title in enumerate(article_titles, 1):
#         print(f"{i}. {title}")
# else:
#     print(f"Failed to retrieve the webpage. Status code: {response.status_code}")


# from selenium import webdriver
# from webdriver_manager.chrome import ChromeDriverManager

# # Use WebDriverManager to automatically download and manage ChromeDriver
# driver = webdriver.Chrome(ChromeDriverManager().install())

# # Rest of your Selenium code
