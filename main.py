import time
import datetime
import requests
import csv
from bs4 import BeautifulSoup

UPDATE_DELAY = 86400

def get_content(element):
    if element:
        return element.get_text().strip()
    else:
        return 'NoneType'

URL = 'https://www.amazon.com.br/HD-SSD-KINGSTON-SA400S37-480GB/dp/B075BKXSCQ/ref=sr_1_4?__mk_pt_BR=ÅMÅŽÕÑ'
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 OPR/99.0.4788.5"}

def update():
    try:
        #get page content
        page = requests.get(URL, headers=headers)
        content = BeautifulSoup(page.content, "html.parser")

        title_element = content.find("span", {"id": "productTitle"})
        title = get_content(title_element)

        price_element = content.find("span", {"class": "a-offscreen"})
        price = get_content(price_element)

        #header structure
        today = datetime.date.today()
        header = ['Title', 'Price', 'Date']
        data = [title, price, today]
        print(header)
        print(data)

        #export to csv
        with open('AmazonWebScraperDataset.csv', 'a+', newline='', encoding='UTF8') as f:
            writer = csv.writer(f)
            writer.writerow(data)

    except requests.exceptions.RequestException as e:
        print("An error occurred:", e)
    except Exception as ex:
        print("An exception occurred:", ex)

while(1):
    update()
    time.sleep(UPDATE_DELAY)