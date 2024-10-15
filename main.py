from config.config import load_config, validate_config, validate_files
from clients.ai_client import initialize_ai_client, create_article, get_ai_model, initialize_image_client
from clients.openai_client import (
    create_assistant, create_vector_store_and_upload_files,
    update_assistant_with_vector_store, instructions, download_image, clean_article_content
)
from clients.perplexity_client import perplexity_research
from upload_to_wordpress import upload_articles_in_directory
from utils.file_utils import save_markdown_file, load_csv_file, load_markdown_file
from clients.wordpress_client import convert_markdown_to_html, upload_to_wordpress, save_html_file
from utils.logging_utils import setup_logging, log_error, log_info
from utils.sitemap_utils import parse_sitemap, parse_sitemap_to_txt
from clients.image_utils import generate_image_sync, generate_image_openai, generate_image_fal
from datetime import datetime
import os
import sys
import time
import shutil
import asyncio
import requests

async def generate_and_save_image(image_client, slug, article_dir, image_provider):
    image_prompt = f"Create a realistic picture that visually represents the content described by the article slug: '{slug}'. The image should be detailed, lifelike, and appropriate for a blog post."

    try:
        if image_provider == "fal":
            image_url = await generate_image_fal(image_client, image_prompt)
        elif image_provider == "openai":
            image_url = generate_image_openai(image_client, image_prompt)
        else:
            raise ValueError(f"Unsupported image provider: {image_provider}")

        image_file = os.path.join(article_dir, f"{slug}_image.png")
        download_image(image_url, image_file)
        print(f"Image for article '{slug}' generated and saved successfully.")
    except Exception as e:
        print(f"Error generating or saving image for '{slug}': {str(e)}")

def download_image(url, file_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(file_path, 'wb') as file:
            file.write(response.content)
        print(f"Image saved to: {file_path}")
    else:
        print(f"Failed to download image. Status code: {response.status_code}")

async def main():
    # Setup logging
    setup_logging()

    #Delay 300 seconds - 300 seconds = 5 minutes
    TIME_DELAY = 300

    # Load and validate configuration
    config = load_config()
    if not validate_config(config):
        log_error("Configuration validation failed. Exiting.")
        return

    if not validate_files(config):
        log_error("File validation failed. Exiting.")
        return

    # Initialize AI client based on the selected provider
    ai_client = initialize_ai_client()
    image_client = initialize_image_client()
    model = get_ai_model()

    # Create or use existing OpenAI assistant (only for OpenAI)
    assistant_id = config.get("OPENAI_ASSISTANT_ID")
    if config["AI_PROVIDER"].lower() == "openai" and not assistant_id:
        assistant_id = create_assistant(
            ai_client,
            name=config.get("BUSINESS_NAME"),
            instructions=instructions,
            model=model
        )

    # Create a directory for today's date
    today = datetime.today().strftime('%Y-%m-%d')
    ai_provider = config["AI_PROVIDER"].lower()
    articles_dir = os.path.join('articles', ai_provider, today)
    os.makedirs(articles_dir, exist_ok=True)

    # Load articles CSV
    articles = load_csv_file(config["ARTICLES_CSV"])

    # Convert sitemap to text file
    sitemap_xml_path = 'data/sitemap_index.xml'
    sitemap_txt_path = 'data/sitemap_index.txt'
    parse_sitemap_to_txt(sitemap_xml_path, sitemap_txt_path)

    # Process each article
    for index, article in enumerate(articles):
        slug = article['slug']
        keywords = article['keywords'].split(';')

        # Create a directory for each article using its slug
        article_dir = os.path.join(articles_dir, slug)

        # Check if the article directory already exists
        if os.path.exists(article_dir):
            print(f"Article directory for '{slug}' already exists. Skipping this article.")
            continue

        # If the directory doesn't exist, create it and process the article
        os.makedirs(article_dir, exist_ok=True)

        # Conduct Perplexity research for each keyword
        research_results = []
        for keyword in keywords:
            keyword = keyword.strip()
            research_result = perplexity_research(keyword, config["PERPLEXITY_API_KEY"])
            if research_result:
                research_results.append(research_result)

        if research_results:
            # Combine research results into one markdown file
            research_content = "\n\n".join([str(result) for result in research_results])
            research_file = os.path.join(article_dir, f"{slug}_perplexity.md")
            save_markdown_file(research_file, research_content)

            # Create a vector store and upload files (only for OpenAI)
            if config["AI_PROVIDER"].lower() == "openai":
                file_paths = [
                    config["KNOWLEDGE_PROFILE_JSON"],
                    'data/example_article.md',
                    sitemap_txt_path,
                    research_file
                ]
                vector_store_id = create_vector_store_and_upload_files(ai_client, file_paths, business_name=config["BUSINESS_NAME"])
                update_assistant_with_vector_store(ai_client, assistant_id, vector_store_id)

            # Parse sitemap for internal links
            sitemap_path = 'data/sitemap_index.xml'
            internal_links = parse_sitemap(sitemap_path)

            # Generate article using the selected AI provider
            business_name = config["BUSINESS_NAME"]
            country = config["COUNTRY"]
            language = config["LANGUAGE"]
            article_content = create_article(
                ai_client, model=model, assistant_id=assistant_id, slug=slug, keywords=keywords,
                research_content=research_content, internal_links=internal_links,
                business_name=business_name, country=country, language=language
            )

            # Check if an error occurred during article creation
            if isinstance(article_content, str) and article_content.startswith("Error:"):
                log_error(f"Error occurred while creating article '{slug}': {article_content}")
                print(f"Error occurred while creating article '{slug}'. Exiting.")
                print("-------------------")
                print(f"Deleting folder '{article_dir}'...")
                shutil.rmtree(article_dir, ignore_errors=True)
                print(f"Folder '{article_dir}' deleted.")
                sys.exit(1)

            # Clean the article content
            article_content = clean_article_content(article_content)

            # Save article to markdown file
            article_file = os.path.join(article_dir, f"{slug}_Article.md")
            save_markdown_file(article_file, article_content)

            # Convert markdown to HTML
            html_content = convert_markdown_to_html(article_content)
            html_file = os.path.join(article_dir, f"{slug}_Article.html")
            save_html_file(html_file, html_content)
            print(f"Article '{slug}' generated successfully.")
            print("-------------------")

            # Generate and save image if enabled
            if config["GENERATE_IMAGES"]:
                await generate_and_save_image(image_client, slug, article_dir, config["IMAGE_PROVIDER"].lower())

        # Implement timeout for Claude
        if config["AI_PROVIDER"].lower() == "claude" and index < len(articles) - 1:
            print(f"Waiting for {TIME_DELAY} seconds before processing the next article...")
            await asyncio.sleep(TIME_DELAY)  # Use asyncio.sleep instead of time.sleep

    # Upload articles to WordPress if enabled
    if config["UPLOAD_TO_WORDPRESS"]:
        articles_folder = 'articles'
        if not os.listdir(articles_folder):
            print("The 'articles' directory is empty. Start Generate new Articles.")
            return
        upload_articles_in_directory(articles_folder)

if __name__ == "__main__":
    asyncio.run(main())
