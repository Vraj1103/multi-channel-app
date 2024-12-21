from fastapi import APIRouter, HTTPException
from app.services.database import get_messages
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
    if not response["ok"]:
        raise HTTPException(status_code=400, detail=response["error"])
    return {"detail": "Message sent successfully", "data": response["message"]}
