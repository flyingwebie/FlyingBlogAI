import openai
import logging

def initialize_openai_client(api_key):
    openai.api_key = api_key
    logging.info("OpenAI client initialized.")
    return openai

def upload_file(client, file_path, purpose):
    with open(file_path, "rb") as file:
        response = client.File.create(file=file, purpose=purpose)
    logging.info(f"File uploaded successfully, ID: {response.id}")
    return response.id

def create_article(client, assistant_id, knowledge_profile_id, research_file_id, example_article):
    prompt = (
        f"Using the knowledge profile with ID {knowledge_profile_id} and the research file with ID {research_file_id}, "
        f"generate a detailed article. Use the example article structure from the provided markdown example."
    )
    response = client.Completion.create(
        model="gpt-4-turbo",
        prompt=prompt,
        max_tokens=2048
    )
    article_content = response.choices[0].text
    logging.info("Article created successfully.")
    return article_content
