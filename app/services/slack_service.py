from app.services.database import save_message
import datetime 
async def handle_event(payload):
    """
    Handles incoming Slack events payload.
    """
    if "challenge" in payload:
        # Respond to Slack's challenge verification during setup
        return {"challenge": payload["challenge"]}
    
    # print(payload,'payload')
    # print(payload.get("event", {}),'payload events')
    # Process Slack Events
    event = payload.get("event", {})
    if event.get("type") == "message" and "subtype" not in event:
        # Extract message data
        message_data = payload
        # Save message to MongoDB
        print("Saving message to MongoDB")
        save_message(message_data)
        print("Message saved")
        return {"ok": True}

    # Event not handled
    return {"ok": False, "error": "Event type not supported"}
