from pydantic import BaseSettings


class Settings(BaseSettings):
    API_STR: str = "/api"
    PROJECT_NAME: str = "execution-template"

    PORT_API_URL: str = "https://api.getport.io/v1"
    PORT_CLIENT_ID: str
    PORT_CLIENT_SECRET: str

    class Config:
        case_sensitive = True


settings = Settings()
