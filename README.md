# test
How to Run This API Locally
🧩 Requirements
Python 3.7+

MongoDB Atlas account or local MongoDB instance

Google Chrome installed (Playwright depends on it)

A MongoDB user with readWrite access to database1

Whitelisted IP or 0.0.0.0/0 in MongoDB Atlas

Step-by-Step Setup
Install dependencies:

bash
Copy
Edit
pip install flask pymongo playwright
playwright install
Run your app:
Save your script as app.py, then run:

bash
Copy
Edit
python app.py
Use the API:
Call the API in a browser or tool like curl or Postman:

bash
Copy
Edit
curl "http://localhost:5000/extract?search_key=Tata&company_name=Tata%20Advanced%20Systems%20Limited"
MongoDB Setup Tips
 Create a User in MongoDB Atlas
Go to Security > Database Access > Add New Database User

Username: kumaraman8594

Password: Sairam@8594 (Valid for 24 hr)

Database Access: Read and write to any database or specific database1

Network Whitelist
Go to Security > Network Access

Add IP Address: 0.0.0.0/0 (for development only) or your specific IP.(Valid for 24 hr)



"learned about  playwright and dumping the data in mongo by creating Db giving access and all.
It was interesting."
