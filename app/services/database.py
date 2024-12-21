from pymongo import MongoClient
from app.config import settings
from bson.json_util import dumps


client = MongoClient(settings.mongodb_uri)
if client:
    print("Connected to MongoDB")
db = client.get_database("slack_bot")
messages_collection = db.get_collection("messages")

def save_message(message_data):
    try:
        if message_data:
            messages_collection.insert_one(message_data)
        else:
            print("No message data to save")
    except Exception as e:
        print(f"Error saving message: {e}")

def get_messages():
    try:
        # print("In get_messages")
        # Fetch all documents from the collection

        messages_cursor = messages_collection.find({}, {"timestamp": 1, "text": 1, "user": 1, "_id": 0})

        # Convert cursor to a list
        messages = list(messages_cursor)
        messages_json = dumps(messages)
        # The line `# print(f"Messages fetched: {messages_json}")` is a commented-out line of code in
        # Python. It is using string formatting to include the variable `messages_json` in the printed
        # message. However, since the line is commented out with `#`, it will not be executed when the
        # code runs.
        # print(f"Messages fetched: {messages_json}")
        return messages_json
    except Exception as e:
        print(f"Error fetching messages: {e}")
        return []
