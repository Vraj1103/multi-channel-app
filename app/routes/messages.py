from fastapi import APIRouter
from app.services.database import get_messages

router = APIRouter()

@router.get("/")
async def fetch_messages():
    # print("Fetching messages")
    messages =  get_messages()
    return {"messages": messages}
