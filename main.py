import time
import datetime
import requests
import pandas as pd
from bs4 import BeautifulSoup

UPDATE_DELAY = 86400

def get_content(element):
    if element:
        return element.get_text().strip()
    else:
        return 'NoneType'

url = 'https://www.amazon.com.br/s?k=ssd'
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 OPR/98.0.0.0"
}

data_list = []  # List to store the scraped data

def update(url):
    try:
        # Get page content
        page = requests.get(url, headers=headers)
        content = BeautifulSoup(page.content, "html.parser")

        products = content.find_all("div", {"data-component-type": "s-search-result"})

        for product in products:
            title_element = product.find("span", {"class": "a-size-base-plus a-color-base a-text-normal"})
            title = get_content(title_element)

            price_element = product.find("span", {"class": "a-price-whole"})
            price = get_content(price_element)

            rating_element = product.find("span", {"class": "a-icon a-icon-star-small a-star-small-5 aok-align-bottom"})
            rating = get_content(rating_element)

            url_element = product.find("a", {"class": "a-link-normal s-no-outline"})
            product_url = url_element["href"]

            today = datetime.date.today()

            data_dict = {
                'Title': title,
                'Price': price,
                'Rating': rating,
                'URL': product_url,
                'Date': today
            }

            data_list.append(data_dict)  # Add the data dictionary to the list

            print(data_dict)  # Print the dictionary for verification

    except requests.exceptions.RequestException as e:
        print("An error occurred:", e)
    except Exception as ex:
        print("An exception occurred:", ex)

def next_page(content):
    next_link = content.find("a", {"class": "s-pagination-item s-pagination-next s-pagination-button s-pagination-separator"})
    if next_link and not next_link.find("span", {"class": "s-pagination-item s-pagination-next s-pagination-disabled"}):
        url_next = 'https://www.amazon.com.br' + next_link['href']
        return url_next
    else:
        return None

# Start scraping process
current_url = url
while current_url:
    update(current_url)
    current_url = next_page(BeautifulSoup(requests.get(current_url, headers=headers).content, "html.parser"))
    time.sleep(UPDATE_DELAY)

# Convert the data list to a DataFrame
df = pd.DataFrame(data_list)

# Export the DataFrame to a CSV file
df.to_csv('AmazonWebScraperDataset.csv', index=False)