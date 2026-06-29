from openai import OpenAI

from app.core.config import settings


def create_client():

    return OpenAI(
        base_url=settings.azure_openai_endpoint,
        api_key=settings.azure_openai_key,
    )