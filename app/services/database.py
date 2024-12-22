from pymongo import MongoClient
from app.config import settings
# from bson.json_util import dumps
# import json

client = MongoClient(settings.mongodb_uri)
if client:
    print("Connected to MongoDB")
db = client.get_database("slack_bot")
db_sms = client.get_database("sms_bot")
db_whatsapp = client.get_database("whatsapp_bot")
slack_messages_collection = db.get_collection("messages")
sms_messages_collection = db_sms.get_collection("messages")
whatsapp_messages_collection = db_whatsapp.get_collection("messages")

def save_message(message_data,app:str):
    if app == "slack":
        try:
            if message_data:
                slack_messages_collection.insert_one(message_data)
            else:
                print("No message data to save")
        except Exception as e:
            print(f"Error saving message: {e}")
    elif app == "sms":
        try:
            if message_data:
                sms_messages_collection.insert_one(message_data)
            else:
                print("No message data to save")
        except Exception as e:
            print(f"Error saving message: {e}")
    elif app == "whatsapp":
        try:
            if message_data:
                whatsapp_messages_collection.insert_one(message_data)
            else:
                print("No message data to save")
        except Exception as e:
            print(f"Error saving message: {e}")


def get_messages(app: str):
    """
    Fetch all messages for a specific app.
    """
    try:
        if app == "slack":
            messages_cursor = slack_messages_collection.find({}, {"_id": 0, "timestamp": 1, "text": 1, "user": 1})
        elif app == "sms":
            messages_cursor = sms_messages_collection.find({}, {"_id": 0, "timestamp": 1, "text": 1, "user": 1})
        elif app == "whatsapp":
            messages_cursor = whatsapp_messages_collection.find({}, {"_id": 0, "timestamp": 1, "text": 1, "user": 1})
        else:
            return []

        return list(messages_cursor)  # Convert cursor to a list
    except Exception as e:
        print(f"Error fetching messages for {app}: {e}")
        return []
