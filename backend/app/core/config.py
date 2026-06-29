from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    database_url: str
    azure_openai_endpoint: str
    azure_openai_key: str
    azure_openai_deployment: str
    
    
    azure_doc_intelligence_endpoint: str
    azure_doc_intelligence_key: str

    google_client_id: str
    google_client_secret: str
    google_redirect_uri: str
    class Config:
        env_file = ".env"


settings = Settings()