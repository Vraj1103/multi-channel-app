from fastapi import FastAPI
from app.routes import slack, messages,twilio_routes,whatsapp_routes

app = FastAPI()

# Include API Routes
app.include_router(slack.router, prefix="/slack", tags=["Slack"])
app.include_router(messages.router, prefix="/messages", tags=["Messages"])
app.include_router(twilio_routes.router, prefix="/twilio", tags=["Twilio"])
app.include_router(whatsapp_routes.router, prefix="/whatsapp", tags=["WhatsApp"])

@app.get("/")
async def root():
    return {"message": "Slack Chat App is running!"}
