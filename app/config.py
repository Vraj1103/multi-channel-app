from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    mongodb_uri: str
    slack_bot_token: str
    slack_signing_secret: str
    twilio_account_sid: str
    twilio_auth_token: str
    twilio_phone_number: str
    twilio_whatsapp_number: str 

    class Config:
        env_file = ".env"

settings = Settings()
