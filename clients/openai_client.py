import openai
import logging

def initialize_openai_client(api_key):
    openai.api_key = api_key
    logging.info("OpenAI client initialized.")
    return openai

def upload_file(client, file_path, purpose):
    with open(file_path, "rb") as file:
        response = client.File.create(file=file, purpose=purpose)
    logging.info(f"File uploaded successfully, ID: {response['id']}")
    return response['id']

def create_assistant(client, name, instructions, model):
    response = client.Assistant.create(
        name=name,
        instructions=instructions,
        model=model
    )
    assistant_id = response['id']
    logging.info(f"Assistant created successfully, ID: {assistant_id}")
    return assistant_id

def create_article(client, assistant_id, knowledge_profile_id, research_file_id, example_article, internal_links):
    prompt = (
        f"Using the knowledge profile with ID {knowledge_profile_id} and the research file with ID {research_file_id}, "
        f"generate a detailed article. Use the example article structure from the provided markdown example. "
        f"Incorporate the following internal links where appropriate: {internal_links}"
    )
    response = client.Completion.create(
        model="gpt-4-turbo",
        prompt=prompt,
        max_tokens=2048
    )
    article_content = response.choices[0].text
    logging.info("Article created successfully.")
    return article_content