import os
from dotenv import load_dotenv
from clients.openai_client import initialize_openai_client, create_article as create_openai_article
from clients.claude_client import initialize_claude_client, create_article as create_claude_article

load_dotenv()

def initialize_image_client():
    image_provider = os.getenv("IMAGE_PROVIDER", "openai").lower()

    if image_provider == "openai":
        api_key = os.getenv("OPENAI_API_KEY")
        return initialize_openai_client(api_key)
    else:
        raise ValueError(f"Unsupported image provider: {image_provider}")

def initialize_ai_client():
    ai_provider = os.getenv("AI_PROVIDER", "openai").lower()

    if ai_provider == "openai":
        api_key = os.getenv("OPENAI_API_KEY")
        return initialize_openai_client(api_key)
    elif ai_provider == "claude":
        api_key = os.getenv("CLAUDE_API_KEY")
        return initialize_claude_client(api_key)
    else:
        raise ValueError(f"Unsupported AI provider: {ai_provider}")

def get_ai_model():
    ai_provider = os.getenv("AI_PROVIDER", "openai").lower()

    if ai_provider == "openai":
        return os.getenv("OPENAI_MODEL", "gpt-4o")
    elif ai_provider == "claude":
        return os.getenv("CLAUDE_MODEL", "claude-3-5-sonnet-20240620")
    else:
        raise ValueError(f"Unsupported AI provider: {ai_provider}")

def create_article(client, **kwargs):
    ai_provider = os.getenv("AI_PROVIDER", "openai").lower()
    model = get_ai_model()

    if ai_provider == "openai":
        return create_openai_article(client, **kwargs)
    elif ai_provider == "claude":
        return create_claude_article(client, **kwargs)
    else:
        raise ValueError(f"Unsupported AI provider: {ai_provider}")
