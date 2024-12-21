from fastapi import APIRouter, Request, HTTPException
from app.utils.slack_verification import verify_slack_request
from app.services.slack_service import handle_event

router = APIRouter()

@router.post("/events")
async def slack_events(request: Request):
    headers = request.headers
    body = await request.body()

    # Verify request
    verify_slack_request(headers, body)

    payload = await request.json()
    return await handle_event(payload)
