from twilio.rest import Client
from app.services.database import save_message
from app.config import settings

# Initialize Twilio Client
twilio_client = Client(settings.twilio_account_sid, settings.twilio_auth_token)

def send_whatsapp_message(to: str, message: str):
    """
    Sends a WhatsApp message using Twilio's API.

    :param to: The recipient's WhatsApp number (e.g., 'whatsapp:+1234567890').
    :param message: The message text to send.
    :return: Success or error response.
    """
    try:
        # Send message via Twilio's API
        message_response = twilio_client.messages.create(
            from_=settings.twilio_whatsapp_number,
            to=to,
            body=message
        )
        
        # Save the sent message to the database
        message_data = {
            "user": "BOT",
            "platform": "whatsapp",
            "channel_id": to,
            "text": message,
            "timestamp": message_response.date_created.isoformat()
        }
        save_message(message_data,"whatsapp")

        print(f"WhatsApp message sent successfully: {message_response.sid}")
        return {"ok": True, "message": message, "sid": message_response.sid}
    except Exception as e:
        print(f"Error sending WhatsApp message: {e}")
        return {"ok": False, "error": str(e)}
