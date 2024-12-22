from fastapi import APIRouter, HTTPException, Request
from app.services.whatsapp_service import send_whatsapp_message
from app.services.database import save_message
from pydantic import BaseModel

router = APIRouter()
class WhatsappMessageRequest(BaseModel):
    to: str
    body: str

@router.post("/send-whatsapp-message")
def send_message_to_whatsapp(payload: WhatsappMessageRequest):
    """
    API to send a message to a WhatsApp user.

    :param to: Recipient's WhatsApp number (e.g., 'whatsapp:+1234567890').
    :param text: Message text.
    :return: Success or error response.
    """
    response = send_whatsapp_message(payload.to, payload.body)
    if not response["ok"]:
        raise HTTPException(status_code=400, detail=response["error"])
    return {"detail": "Message sent successfully", "data": response["message"]}

@router.post("/receive-message")
async def whatsapp_webhook(request: Request):
    """
    Webhook to handle incoming WhatsApp messages from Twilio.
    """
    try:
        # Parse incoming request from Twilio
        data = await request.form()
        # print(f"Received WhatsApp message: {data}")
        message_data = {
            "user_name":data.get("ProfileName"),
            "user": data.get("From"),
            "channel_id": data.get("To"),
            "text": data.get("Body"),
            "timestamp": data.get("Timestamp"),
            "platform": "whatsapp"
        }

        # Save message to MongoDB
        save_message(message_data,"whatsapp")
        print(f"Incoming WhatsApp message: {message_data}")

        # Respond to Twilio (mandatory)
        return {"message": "Message received successfully!"}

    except Exception as e:
        print(f"Error processing webhook: {e}")
        return {"error": str(e)}
