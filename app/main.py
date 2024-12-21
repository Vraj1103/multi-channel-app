from fastapi import FastAPI
from app.routes import slack, messages

app = FastAPI()

# Include API Routes
app.include_router(slack.router, prefix="/slack", tags=["Slack"])
app.include_router(messages.router, prefix="/messages", tags=["Messages"])

@app.get("/")
async def root():
    return {"message": "Slack Chat App is running!"}
