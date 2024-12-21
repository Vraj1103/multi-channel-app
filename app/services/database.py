from pymongo import MongoClient
from app.config import settings

# Initialize MongoDB Client
client = MongoClient(settings.mongodb_uri)
db = client.get_database("slack_bot")

# Collections
messages_collection = db.get_collection("messages")

# Save Message to MongoDB
def save_message(message_data):
    try:
        if message_data:
            messages_collection.insert_one(message_data)
            print(f"Message saved: {message_data}")
        else:
            print("No message data to save")
    except Exception as e:
        print(f"Error saving message: {e}")

# Retrieve All Messages
def get_messages():
    try:
        if messages_collection: 
            return list(messages_collection.find({}, {"_id": 0}))
        else:
            print("No messages found")
            return []
    except Exception as e:
        print(f"Error fetching messages: {e}")
        return []