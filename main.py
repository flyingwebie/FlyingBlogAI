from config.config import load_config, validate_config, validate_files
from clients.openai_client import (
    initialize_openai_client, create_assistant, create_vector_store_and_upload_files,
    update_assistant_with_vector_store, create_article, instructions
)
from clients.perplexity_client import perplexity_research
from utils.file_utils import save_markdown_file, load_csv_file, load_markdown_file
from clients.wordpress_client import convert_markdown_to_html, upload_to_wordpress, save_html_file
from utils.logging_utils import setup_logging, log_error, log_info
from utils.sitemap_utils import parse_sitemap, parse_sitemap_to_txt
from datetime import datetime
import os

def main():
    # Setup logging
    setup_logging()

    # Load and validate configuration
    config = load_config()
    if not validate_config(config):
        log_error("Configuration validation failed. Exiting.")
        return

    if not validate_files(config):
        log_error("File validation failed. Exiting.")
        return

    # Initialize OpenAI client
    openai_client = initialize_openai_client(config["OPENAI_API_KEY"])
    model = config["MODEL"]

    # Create or use existing OpenAI assistant
    assistant_id = config.get("OPENAI_ASSISTANT_ID")
    if not assistant_id:
        assistant_id = create_assistant(
            openai_client,
            name=config.get("BUSINESS_NAME"),
            instructions=instructions,
            model=model
        )

    # Create a directory for today's date
    today = datetime.today().strftime('%Y-%m-%d')
    articles_dir = os.path.join('articles', today)
    os.makedirs(articles_dir, exist_ok=True)

    # Load articles CSV
    articles = load_csv_file(config["ARTICLES_CSV"])

    # Convert sitemap to text file
    sitemap_xml_path = 'data/sitemap_index.xml'
    sitemap_txt_path = 'data/sitemap_index.txt'
    parse_sitemap_to_txt(sitemap_xml_path, sitemap_txt_path)

    # Process each article
    for article in articles:
        slug = article['slug']
        keywords = article['keywords'].split(',')

        # Create a directory for each article using its slug
        article_dir = os.path.join(articles_dir, slug)
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

            # Create a vector store and upload files (knowledge profile, example article, sitemap, and research files)
            file_paths = [
                config["KNOWLEDGE_PROFILE_JSON"],
                'data/example_article.md',
                sitemap_txt_path,
                research_file
            ]

            vector_store_id = create_vector_store_and_upload_files(openai_client, file_paths, business_name=config["BUSINESS_NAME"])

            # Update assistant to use the vector store
            update_assistant_with_vector_store(openai_client, assistant_id, vector_store_id)

            # Parse sitemap for internal links
            sitemap_path = 'data/sitemap_index.xml'
            internal_links = parse_sitemap(sitemap_path)

            # Generate article using OpenAI assistant
            business_name = config["BUSINESS_NAME"]
            country = config["COUNTRY"]
            language = config["LANGUAGE"]
            article_content = create_article(
                openai_client, model, assistant_id, slug, keywords, research_content, internal_links, business_name, country, language
            )

            # Save article to markdown file
            article_file = os.path.join(article_dir, f"{slug}_Article.md")
            save_markdown_file(article_file, article_content)

            # Convert markdown to HTML
            html_content = convert_markdown_to_html(article_content)
            html_file = os.path.join(article_dir, f"{slug}_Article.html")
            save_html_file(html_file, html_content)

            # Upload article to WordPress if enabled
            if config["UPLOAD_TO_WORDPRESS"]:
                upload_to_wordpress(
                    config["WORDPRESS_USERNAME"], config["WORDPRESS_PASSWORD"],
                    config["WORDPRESS_API_URL"], f"Article on {', '.join(keywords)}", html_content
                )

if __name__ == "__main__":
    main()
