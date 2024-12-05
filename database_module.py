
# database_module.py
from pymongo import MongoClient

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/med_database')  # Replace with your MongoDB URI
db = client['medicine_database']
collection = db['medicines']

# Insert medicine into the database
def insert_medicine(product_name, generic_name, expiry_date, category):
    medicine = {
        'product_name': product_name,
        'generic_name': generic_name,
        'expiry_date': expiry_date,
        'category': category
    }
    collection.insert_one(medicine)

# Fetch medicines from the database
def fetch_medicines():
    medicines = collection.find()
    return list(medicines)
