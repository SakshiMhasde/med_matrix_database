from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from validation_module import compare_data  # Importing the validation function
from datetime import datetime

app = Flask(__name__)

# Set up the MongoDB connection (adjust this to your actual MongoDB URI)
app.config["MONGO_URI"] = "mongodb://localhost:27017/med_database"
mongo = PyMongo(app)

@app.route('/')
def dashboard():
    # Fetch all medicine data from the MongoDB collection
    all_meds = list(mongo.db.medicines.find())  # Ensure we get a list of documents
    
    consumable_meds = [med for med in all_meds if med.get('Type') == 'Consumable']
    non_consumable_meds = [med for med in all_meds if med.get('Type') == 'Non-Consumable']

    # Pass all medicines to the dashboard template
    return render_template(
        'dashboard.html', 
        all_meds=all_meds,  # Pass all medicines to the dashboard template
        consumable_meds=consumable_meds, 
        non_consumable_meds=non_consumable_meds
    )

@app.route('/reason/<med_id>')
def reason(med_id):
    # Fetch the medicine document by its ID
    med = mongo.db.medicines.find_one({"_id": ObjectId(med_id)})

    if not med:
        return "Medicine not found", 404

    # Dummy OCR data for demonstration purposes (replace with actual OCR input)
    ocr_data = {
        "Product Name": med.get("Product Name"),
        "Generic Name": med.get("Generic Name"),
        "Expiry Date": med.get("Expiry Date").strftime('%Y-%m-%d') if isinstance(med.get("Expiry Date"), datetime) else med.get("Expiry Date"),
        "Type": med.get("Type"),
    }

    # Validate data using the compare_data function
    mismatched_data, is_valid, message = compare_data(ocr_data, med)

    return render_template('reason.html', med=med, mismatched_data=mismatched_data, message=message)

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Handle file upload and processing here (TBD)
        return redirect(url_for('dashboard'))

    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)
