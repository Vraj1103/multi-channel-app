from twilio.rest import Client
from app.services.database import save_message
from app.config import settings

# Initialize Twilio client
twilio_client = Client(settings.twilio_account_sid, settings.twilio_auth_token)

def send_sms(to: str, body: str):
    """
    Send an SMS using Twilio and store the message in the database.

    :param to: The recipient's phone number (in E.164 format, e.g., +1234567890).
    :param body: The message text to send.
    :return: Success or error response.
    """
    try:
        # Send SMS
        message = twilio_client.messages.create(
            to=to,
            from_=settings.twilio_phone_number,
            body=body
        )
        print(f"Message sent successfully: {message.sid}")

        # Save the sent message to MongoDB
        message_data = {
            "user": "BOT",  # Indicating that this message was sent by the bot
            "to": to,
            "text": body,
            "timestamp": message.date_created.isoformat(),
            "platform": "sms"
        }
        save_message(message_data,"sms")

        return {"ok": True, "sid": message.sid}
    except Exception as e:
        print(f"Error sending SMS: {e}")
        return {"ok": False, "error": str(e)}
