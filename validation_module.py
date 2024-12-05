from datetime import datetime

def compare_data(ocr_data, mongo_data):
    mismatched_data = []
    is_valid = True
    message = ""

    # If mongo_data is a list, use the first element (assuming only one document)
    if isinstance(mongo_data, list):
        if len(mongo_data) > 0:
            mongo_data = mongo_data[0]  # Use the first document
        else:
            return mismatched_data, False, "No data found in MongoDB"

    for key, ocr_value in ocr_data.items():
        db_value = mongo_data.get(key)

        # Handle date comparisons separately
        if key == "Expiry Date":
            if isinstance(db_value, datetime):
                db_value_str = db_value.strftime('%Y-%m-%d')  # Format date for comparison
                ocr_value_str = ocr_value.strip()  # Assuming OCR returns a string
                if ocr_value_str != db_value_str:
                    mismatched_data.append((key, ocr_value_str, db_value_str))
                    is_valid = False
            else:
                mismatched_data.append((key, ocr_value, db_value))
                is_valid = False
        else:
            if ocr_value.strip().lower() != str(db_value).strip().lower():
                mismatched_data.append((key, ocr_value, db_value))
                is_valid = False

    if not is_valid:
        message = "Data mismatch found."
    else:
        message = "Data verified successfully."

    return mismatched_data, is_valid, message
