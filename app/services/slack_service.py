from app.services.database import save_message
import datetime 
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from app.config import settings

slack_client = WebClient(token=settings.slack_bot_token)

def get_user_info(user_id: str):
    """
    Fetch user information from Slack using the user ID.
    
    :param user_id: Slack user ID.
    :return: User information or an error message.
    """
    try:
        response = slack_client.users_info(user=user_id)
        user_info = response.get("user", {})
        print(f"User info retrieved: {user_info}")
        return user_info
    except SlackApiError as e:
        print(f"Error fetching user info: {e.response['error']}")
        return None


def get_user_name(user_id: str):
    """
    Get the username or display name of a user.

    :param user_id: Slack user ID.
    :return: User's name (username or display name).
    """
    user_info = get_user_info(user_id)
    if user_info:
        return user_info.get("profile", {}).get("display_name") or user_info.get("real_name")
    return None

async def handle_event(payload):
    """
    Handles incoming Slack events payload.
    """
    if "challenge" in payload:
        return {"challenge": payload["challenge"]}
    
    event = payload.get("event", {})
    if event.get("type") == "message" and "subtype" not in event:
        message_data = payload
        user_id = payload["event"]["user"]
        user_name = get_user_name(user_id)
        message_data = {"user_name": user_name,"platform":"slack", **message_data}
        # message_data = {
        #     "user_name": user_name,
        #     "user_id": payload["event"]["user"],
        #     "channel_id": payload["event"]["channel"],
        #     "text": payload["event"]["text"],
        #     "timestamp": payload['event']['event_ts'],
        #     "team_id": payload["team_id"],
        #     "channel_type": payload["event"]["channel_type"],
        #     "platform": "slack"
        # }
        # Save message to MongoDB
        # print("Saving message to MongoDB")
        save_message(message_data,"slack")
        # print("Message saved")
        return {"ok": True}
    # Event not handled
    return {"ok": False, "error": "Event type not supported"}

def send_message(channel_id: str, text: str):
    """
    Sends a message to a specified Slack channel or user.

    :param channel_id: The channel or user ID where the message will be sent.
    :param text: The message text to send.
    :return: The response from Slack or an error message.
    """
    try:
        # print(f"Sending message to {channel_id}")
        response = slack_client.chat_postMessage(channel=channel_id, text=text)
        # print(f"Message sent successfully: {response['message']}")
        return {"ok": True, "message": response["message"]}
    except SlackApiError as e:
        print(f"Error sending message: {e.response['error']}")
        return {"ok": False, "error": e.response['error']}
