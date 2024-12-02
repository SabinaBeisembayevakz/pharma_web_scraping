import random
import time
import pandas as pd
import os

from datetime import datetime
from bs4 import BeautifulSoup as bs
from cloud_storage import *
from load_to_bq import *
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

os.environ["DISPLAY"]=":99"

def drop_dublicates(x):
    return list(dict.fromkeys(x))


def scraper(browser):
    items=[]
    errs = []
    links1=[]
    urls=[]

    url = 'https://rauza-ade.kz/catalog'
    browser.get(url)
    time.sleep(2)

    page_num = len(browser.find_elements(By.CSS_SELECTOR, 'div.page'))
    if page_num == 0:
        print("Oops! The website seems to be blocked!")
    else:
        print("Got the pages number!")
        for num in range (1,page_num+1):
        # for num in range (1,2):
            page = url + '?p=' + str(num) + '&sort=popularity'
            urls.append(page)
            print("Page "+ str(num) + " -> " + str(page))

        for u in urls:
            browser.get(u)
            time.sleep(2)
            elem1 = browser.find_elements(By.CSS_SELECTOR, 'a.row')
        
            for i in elem1:
                li = i.get_attribute('href')
                # print(i.text)
                links1.append(li)

        links1 = drop_dublicates(links1)
        print(links1)
        print('Collected links ' + str(len(links1)))
        for l in range(0, len(links1)):
            try:
                thelink = links1[l]
                cats = []
                print(thelink)
                browser.get(thelink)
                time.sleep(2)
                c = browser.find_elements(by=By.CSS_SELECTOR, value='a')
                for i in c:
                    try:
                        if '/catalog/' in i.get_attribute('href'):
                            cats.append(i.text)
                    except:
                        cats.append('')
                cat1 = cats[1]
                cat2 = cats[2]
                cat3 = cats[3]
                name = browser.find_elements(by=By.CSS_SELECTOR, value='h1.title')[0].text
                madein = browser.find_elements(by=By.CSS_SELECTOR, value='span.key')[0].text
                company = browser.find_elements(by=By.CSS_SELECTOR, value='span.key')[1].text
                price = browser.find_elements(by=By.CSS_SELECTOR, value='span.price')[0].text
                dict_set = {
                    'category':cat1,
                    'subcategory': cat2,
                    'group': cat3,
                    'name': name,
                    'country': madein,
                    'company':company,
                    'price':price,
                    'url':thelink
                }
                items.append(dict_set)
                print(str(l) + "/" + str(len(links1)) + " scraped links")
            except:
                print("Link " + str(l) + " has errors")
                errs.append(thelink)

    df = pd.DataFrame(items)
    df['date'] = datetime.today()
    if len(errs) > 0:
        dferr = pd.DataFrame(errs)
        dferr.to_excel('rauza-errs-links.xlsx')

    print(str(len(errs))+' ERROR LINKS')       
    print(df.head())
   
    browser.close()
    browser.quit() 
    return(df)


def main():
    
    project_name = 'project_name'
    dataset_name = 'rauza_ade'
    cloud_storage = 'rauza-ade'

    chrome_options = Options()
    path = './chromedriver'
    browser = webdriver.Chrome(path, chrome_options=chrome_options)
    df = scraper(browser)
    df_raw = df.copy()
    df_to_cloudstorage(cloud_storage, dataset_name, df_raw)
    x = df['price'].replace(to_replace=' ', value='', regex=True)
    y = x.replace(to_replace='₸', value='', regex=True)
    df['price'] = [float(x) for x in y]
    print(df.head())
    load_to_bq(project_name, dataset_name, df)   

main()
