from pymongo import MongoClient
from app.config import settings
# from bson.json_util import dumps
# import json

client = MongoClient(settings.mongodb_uri)
if client:
    print("Connected to MongoDB")
db = client.get_database("slack_bot")
slack_messages_collection = db.get_collection("messages")

def save_message(message_data,app:str):
    if app == "slack":
        try:
            if message_data:
                slack_messages_collection.insert_one(message_data)
            else:
                print("No message data to save")
        except Exception as e:
            print(f"Error saving message: {e}")

def get_messages(app:str):
    if app == "slack":
        try:
            # print("In get_messages")
            # Fetch all documents from the collection

            messages_cursor = slack_messages_collection.find({}, {"timestamp": 1, "text": 1, "user": 1, "_id": 0})

            # Convert cursor to a list
            messages = list(messages_cursor)
            # messages_json = json.dumps(messages)
            return messages
        except Exception as e:
            print(f"Error fetching messages: {e}")
            return []
