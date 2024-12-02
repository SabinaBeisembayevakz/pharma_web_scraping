import os
import time
import datetime
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from cloud_storage import *
from load_to_bq import *
import unicodedata2

os.environ["DISPLAY"]=":99"

def scraper (browser):
    list_urls = []
    data = []

    url = "https://europharma.kz"
    browser.get(url)
    time.sleep(5)
    print("Зашёл на Сайт")

    link = browser.find_element(By.CLASS_NAME,'city-confirm__btn-confirm') 
    link.click()
    print("Выбран Город")

    try1 = browser.find_element(By.XPATH,'//a[@class="nav__link js-dropdown-trigger"]')
    browser.execute_script("arguments[0].click();", try1)
    #press the button Katalog

    urls=browser.find_elements(By.XPATH,"//*[@class='menu__link']")
    for u in urls:
        li=u.get_attribute('href')
        list_urls.append(li)
    print(list_urls)

    for i in range(0, len(list_urls),1):
    # for i in range(0,3,1):
        Sub_urls = []
        New_urls = []

        browser.get(list_urls[i])
        time.sleep(3)
        b=1
        # while True:
        for i in range (1,2):
            content = browser.page_source
            soup = BeautifulSoup(content, features="html.parser")
            
            for i in soup.findAll("div", class_="catalog-list__item"):
                link = i.find("a", href = True)
                Sub_urls.append(link['href'])
                
            time.sleep(4)

            try: 
                Page2 = browser.find_element(by=By.XPATH, value='//a[@data-page="'+str(b)+'"]')
                browser.execute_script("arguments[0].click();", Page2)
                b = b + 1
            except:
                break
        for i in Sub_urls:
            helper = str(url) + str(i)
            New_urls.append(helper)
        print(len(New_urls))

        for i in New_urls[0:2]:
            browser.get(i)
            content = browser.page_source
            soup = BeautifulSoup(content, features="html.parser")
            a1 = browser.find_elements(By.XPATH,"//span[@itemprop='name']")
            
            for i in soup.findAll("div", class_="product-detail"):
                Name = i.find("h1", class_="product__title").text
                Country = i.findAll("dd", class_="characteristic__value")[2].text
                Cost = i.find("span", class_="product__price-value").text
                try:
                    category = a1[2].text
                except:
                    category = ""
                try:
                    subCategory = a1[3].text
                except:
                    subCategory = ""
                day_today = datetime.today()
                items = {
                    'name': Name,
                    'country': Country,
                    'price': Cost,
                    'category': category,
                    'subcategory': subCategory,
                    'date':day_today
                }

                data.append(items)

    df = pd.DataFrame(data)

    browser.close()
    browser.quit()

    return df

def main():
    project_name = 'project_name'
    dataset_name = 'europharma'
    cloud_storage = 'europharma'

    chrome_options = webdriver.ChromeOptions()
    path = './chromedriver'
    browser = webdriver.Chrome(executable_path=path, options = chrome_options)

    df = scraper(browser)

    df_raw = df.copy()
    df_to_cloudstorage(cloud_storage, dataset_name, df_raw)
    x = df['price']
    x = x.replace(to_replace='₸', value='', regex=True).values
    x = [unicodedata2.normalize('NFKD', str(x[i])).replace(' ','') for i in range (0, len(x))]
    df['price'] = [float(i) for i in x]
    print(df.head())
    load_to_bq(project_name, dataset_name, df)

main()

