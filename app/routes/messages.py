from fastapi import APIRouter, HTTPException
from app.services.database import get_messages,save_message
from app.services.slack_service import send_message
from pydantic import BaseModel

class MessageRequest(BaseModel):
    channel_id: str
    text: str

router = APIRouter()

@router.get("/")
async def fetch_messages():
    # print("Fetching messages")
    messages =  get_messages("slack")
    return {"messages": messages}

@router.post("/send-message")
def send_message_to_user(payload: MessageRequest):
    """
    API to send a message to a specified Slack channel or user.
    
    :param channel_id: Slack channel or user ID.
    :param text: Message text.
    :return: Success or error response.
    """
    response = send_message(payload.channel_id, payload.text)
    save_message(payload,"slack")
    if not response["ok"]:
        raise HTTPException(status_code=400, detail=response["error"])
    return {"detail": "Message sent successfully", "data": response["message"]}


# API for Slack messages
@router.get("/slack/messages")
async def get_slack_messages():
    """
    API to fetch all Slack messages.
    """
    try:
        messages = get_messages("slack")
        return {"platform": "slack", "messages": messages}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching Slack messages: {str(e)}")

# API for SMS messages
@router.get("/sms/messages")
async def get_sms_messages():
    """
    API to fetch all SMS messages.
    """
    try:
        messages = get_messages("sms")
        return {"platform": "sms", "messages": messages}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching SMS messages: {str(e)}")

# API for WhatsApp messages
@router.get("/whatsapp/messages")
async def get_whatsapp_messages():
    """
    API to fetch all WhatsApp messages.
    """
    try:
        messages = get_messages("whatsapp")
        return {"platform": "whatsapp", "messages": messages}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching WhatsApp messages: {str(e)}")
