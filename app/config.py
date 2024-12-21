from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    mongodb_uri: str
    slack_bot_token: str
    slack_signing_secret: str

    class Config:
        env_file = ".env"

settings = Settings()
