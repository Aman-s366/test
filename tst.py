# import html
# import json
# import re
# from json import JSONDecoder
#
# import requests
# import xmltojson
# from bs4 import BeautifulSoup
# import urllib.parse
#
# url ='https://www.indiaratings.co.in/'
#
# # response  = requests.get(url)
# #
import os

from pymongo import MongoClient
from requests import Session



# MongoDB database connection creation
def set_connection_mongodb():
    # mongo_uri="mongodb://localhost:27017/"
    collection_name = ''
    connection_string = "mongodb+srv://kumaraman8594:t7t6q1s5kLnSNxqJ@cluster0.8nzefzc.mongodb.net/"
    client = MongoClient(connection_string)  # mongoDB connection
    db_name = os.getenv('database1')
    db = client.get_database(db_name)
    return client, db

import requests
from bs4 import BeautifulSoup
#
# def fetch_html_and_store():
#     try:
#         base_url = 'https://www.indiaratings.co.in/'
#         search_param = 'TATA'
#         # Send GET request with search parameter
#         params = {'search': search_param}
#         response = requests.get(base_url, params=params)
#         response.raise_for_status()
#
#         # Parse HTML using BeautifulSoup
#         soup = BeautifulSoup(response.text, 'html.parser')
#
#         # Example: extract all items in a list (customize this part)
#         items = []
#         for item in soup.select('.item'):  # Replace `.item` with actual selectors
#             title = item.select_one('.title')  # Replace `.title` with actual selector
#             price = item.select_one('.price')  # Replace `.price` with actual selector
#
#             if title and price:
#                 items.append({
#                     'title': title.get_text(strip=True),
#                     'price': price.get_text(strip=True)
#                 })
#
#         # Connect to MongoDB and insert
#         client, db = set_connection_mongodb
#
#         if items:
#             collection = db.get_collection('company details')
#             collection.insert_many(items)
#             print("Data successfully inserted into MongoDB.")
#         else:
#             print("No items found to insert.")
#
#     except requests.exceptions.RequestException as e:
#         print(f"HTTP Request failed: {e}")
#     except Exception as e:
#         print(f"An error occurred: {e}")

from playwright.sync_api import sync_playwright
import json

def extract_data_for_company(search_key, company_name_match):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Step 1: Load search result page
        search_url = f"https://www.indiaratings.co.in/searchbykey;key={search_key}"
        page.goto(search_url)
        page.wait_for_selector("#tableRatings a.blackcolor")  # Wait for the results

        # Step 2: Find the correct link using Playwright
        links = page.query_selector_all("#tableRatings a.blackcolor")
        target_link = None

        for link in links:
            text = link.inner_text().strip()
            href = link.get_attribute("href")
            if company_name_match.lower() in text.lower():
                target_link = "https://www.indiaratings.co.in" + href
                break

        if not target_link:
            print("Company not found.")
            browser.close()
            return None

        # Step 3: Visit issuer page
        page.goto(target_link)
        page.wait_for_selector("table")  # Wait for data to load

        # Step 4: Extract table data
        rows = page.query_selector_all("table tr")
        data_rows = []

        for row in rows:
            cells = row.query_selector_all("td")
            cell_texts = [cell.inner_text().strip() for cell in cells]
            if cell_texts:
                data_rows.append(cell_texts)

        browser.close()

        result = {
            "company": company_name_match,
            "url": target_link,
            "data": data_rows
        }

        print(json.dumps(result, indent=2))
        return result

# Example usage:
extract_data_for_company("Tata", "Tata Advanced Systems Limited")












# # data = BeautifulSoup(response.text, 'html.parser')
# # # data = JSONDecoder()
# #
# # for i in response:
# #     print(i)
#
# # try:
# params = {'q': 'TATA'}
# encoded_params = urllib.parse.urlencode(params)
# final_url = f'{url}?{encoded_params}'
# print(final_url)
# response  = requests.get(url)
# data = BeautifulSoup(response.text, 'html.parser')
# with open("sample.html", "w") as html_file:
#     html_file.write(data.text)
#
# with open("sample.html", "r") as html_file:
#     html = html_file.read()
#     json_ = xmltojson.parse(html)
#     html_dict = html_to_dict(soup)
#
# with open("data.json", "w") as file:
#     json.dump(json_, file)
#
# print(json_)
# # print(quote)
#
# print(response)
#
#
# # soup = BeautifulSoup(html)
# # script = soup.find('script', text=re.compile('window\.blog\.data'))
# # json_text = re.search(r'^\s*window\.blog\.data\s*=\s*({.*?})\s*;\s*$',
# #                       script.string, flags=re.DOTALL | re.MULTILINE).group(1)
# # final_data = json.loads(json_text)
# # quote = data.find("span", class_="text")
