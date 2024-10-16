import os
from dotenv import load_dotenv
import json
import logging

def str_to_bool(value):
    """
    Convert a string to a boolean.
    """
    return value.lower() in ['true', '1', 't', 'yes', 'y']

# Load configuration from .env file
def load_config():

    # TODO - Remove override=True
    load_dotenv(override=True)

    config = {
        "AI_PROVIDER": os.getenv("AI_PROVIDER", "openai"),
        "IMAGE_PROVIDER": os.getenv("IMAGE_PROVIDER", "openai"),
        "OPENAI_API_KEY": os.getenv('OPENAI_API_KEY'),
        "OPENAI_MODEL": os.getenv('OPENAI_MODEL'),
        "CLAUDE_API_KEY": os.getenv('CLAUDE_API_KEY'),
        "FAL_KEY": os.getenv('FAL_KEY'),
        "CLAUDE_MODEL": os.getenv('CLAUDE_MODEL'),
        "PERPLEXITY_API_KEY": os.getenv('PERPLEXITY_API_KEY'),
        "OPENAI_ASSISTANT_ID": os.getenv('OPENAI_ASSISTANT_ID'),
        "KNOWLEDGE_PROFILE_JSON": os.getenv('KNOWLEDGE_PROFILE_JSON'),
        "ARTICLES_CSV": os.getenv('ARTICLES_CSV'),
        "WORDPRESS_USERNAME": os.getenv('WORDPRESS_USERNAME'),
        "WORDPRESS_PASSWORD": os.getenv('WORDPRESS_PASSWORD'),
        "WORDPRESS_API_URL": os.getenv('WORDPRESS_API_URL'),
        "UPLOAD_TO_WORDPRESS": str_to_bool(os.getenv('UPLOAD_TO_WORDPRESS', 'True')),
        "WORDPRESS_POST_TYPE": os.getenv("WORDPRESS_POST_TYPE", "posts"),
        "BUSINESS_NAME": os.getenv('BUSINESS_NAME'),
        "COUNTRY": os.getenv('COUNTRY'),
        "LANGUAGE": os.getenv('LANGUAGE'),
        "GENERATE_IMAGES": os.getenv("GENERATE_IMAGES").lower() == "true"
    }

    return config

# Validate configuration
def validate_config(config):
    missing_keys = [key for key, value in config.items() if value is None and key != "UPLOAD_TO_WORDPRESS"]
    if missing_keys:
        logging.error(f"Missing configuration for: {', '.join(missing_keys)}")
        return False
    return True

# Validate file existence
def validate_files(config):
    files_to_check = [config["KNOWLEDGE_PROFILE_JSON"], config["ARTICLES_CSV"]]
    missing_files = [file for file in files_to_check if not os.path.exists(file)]
    if missing_files:
        logging.error(f"Missing files: {', '.join(missing_files)}")
        return False
    return True

# Load JSON file
def load_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)



