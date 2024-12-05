from mongoengine import Document, StringField, DateTimeField, BooleanField, connect

# Connect to the database
connect('medmatrix')  # Replace 'medmatrix' with your actual MongoDB database name

class Medicine(Document):
    name = StringField(required=True)
    expiry_date = DateTimeField(required=True)
    batch_number = StringField(required=True)
    consumable = BooleanField(default=True)
    reason = StringField()

    meta = {'collection': 'medicines'}
