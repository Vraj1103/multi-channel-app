from fastapi import APIRouter, HTTPException, Request
from app.services.twilio_service import send_sms
from app.services.database import save_message
from pydantic import BaseModel

router = APIRouter()


class TwilioMessageRequest(BaseModel):
    to: str
    body: str


@router.post("/send-sms")
def send_sms_to_user(payload: TwilioMessageRequest):
    """
    API to send an SMS to a specified phone number.

    :param to: Recipient's phone number (E.164 format).
    :param body: SMS message content.
    :return: Success or error response.
    """
    response = send_sms(payload.to, payload.body)
    if not response["ok"]:
        raise HTTPException(status_code=400, detail=response["error"])
    return {"detail": "SMS sent successfully", "sid": response["sid"]}


@router.post("/receive-sms")
async def receive_sms(request: Request):
    """
    Endpoint to handle incoming SMS from Twilio.

    :param request: The incoming request from Twilio.
    :return: A success response.
    """
    try:
        form_data = await request.form()
        message_data = {
            "user": form_data.get("From"),  # Sender's phone number
            "to": form_data.get("To"),  # Your Twilio number
            "text": form_data.get("Body"),  # Message content
            "timestamp": form_data.get("DateSent"),  # Timestamp of the message
            "platform": "sms"
        }
        # Save the incoming message to MongoDB
        save_message(message_data)
        return {"detail": "Message received and saved"}
    except Exception as e:
        print(f"Error handling incoming SMS: {e}")
        return {"detail": "Failed to process message", "error": str(e)} 
