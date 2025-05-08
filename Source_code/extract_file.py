from urllib.parse import quote_plus

from flask import Flask, request, jsonify
from pymongo import MongoClient
from playwright.sync_api import sync_playwright
import os

app = Flask(__name__)

# MongoDB database connection creation
def set_connection_mongodb():
    # mongo_uri="mongodb://localhost:27017/"
    username = 'kumaraman8594'
    password = quote_plus('Sairam@8594')
    connection_string = f"mongodb+srv://{username}:{password}@cluster0.8nzefzc.mongodb.net/"
    # uri = f"mongodb://{username}:{password}@localhost:27017/mydatabase"
    client = MongoClient(connection_string)  # mongoDB connection
    db_name = 'database1'
    db = client.get_database(db_name)
    return client, db

@app.route('/extract', methods=['GET'])
def extract_data_for_company():
    search_key = request.args.get('search_key')
    company_name = request.args.get('company_name')

    if not search_key or not company_name:
        return jsonify({"error": "Missing parameters: search_key and company_name"}), 400

    # Step 1: Check MongoDB cache
    client, db = set_connection_mongodb()
    collection = db.get_collection('company_details')
    cached = collection.find_one({"company": company_name})
    if cached:
        cached.pop('_id')  # Remove ObjectId for clean JSON
        return jsonify({"source": "mongo_cache", **cached})

    # Step 2: Use Playwright to scrape
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        search_url = f"https://www.indiaratings.co.in/searchbykey;key={search_key}"
        page.goto(search_url)
        try:
            page.wait_for_selector("#tableRatings a.blackcolor", timeout=10000)
        except:
            browser.close()
            return jsonify({"error": "Search results did not load in time"}), 504

        links = page.query_selector_all("#tableRatings a.blackcolor")
        target_link = None
        for link in links:
            text = link.inner_text().strip()
            href = link.get_attribute("href")
            if company_name.lower() in text.lower():
                target_link = "https://www.indiaratings.co.in" + href
                break

        if not target_link:
            browser.close()
            return jsonify({"error": "Company not found"}), 404

        page.goto(target_link)
        page.wait_for_selector("table")

        rows = page.query_selector_all("table tr")
        data_rows = []
        for row in rows:
            cells = row.query_selector_all("td")
            cell_texts = [cell.inner_text().strip() for cell in cells]
            if cell_texts:
                data_rows.append(cell_texts)

        browser.close()

        results = {
            "company": company_name,
            "url": target_link,
            "data": data_rows
        }

        # Step 3: Save to MongoDB
        collection.insert_one(results)

        return jsonify({"source": "scraped", **results})

if __name__ == '__main__':
    app.run(debug=True)
