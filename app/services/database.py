from pymongo import MongoClient
from app.config import settings

# Initialize MongoDB Client
client = MongoClient(settings.mongodb_uri)
db = client["slack_app"]

# Collections
messages_collection = db["messages"]

# Save Message to MongoDB
def save_message(message_data):
    messages_collection.insert_one(message_data)

# Retrieve All Messages
def get_messages():
    return list(messages_collection.find({}, {"_id": 0}))
