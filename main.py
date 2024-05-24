import os
from datetime import datetime
from config.config import load_config, validate_config, validate_files, load_json_file
from clients.openai_client import initialize_openai_client, upload_file, create_article, create_assistant, instructions
from clients.perplexity_client import perplexity_research
from utils.file_utils import save_markdown_file, load_csv_file, load_markdown_file
from clients.wordpress_client import convert_markdown_to_html, upload_to_wordpress
from utils.logging_utils import setup_logging, log_error, log_info
from utils.sitemap_utils import parse_sitemap

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

    # Load knowledge profile JSON
    knowledge_profile = load_json_file(config["KNOWLEDGE_PROFILE_JSON"])

    log_info("Configuration and files validated successfully.")
    log_info(f"Knowledge profile loaded: {knowledge_profile}")

    # Initialize OpenAI client
    openai_client = initialize_openai_client(config["OPENAI_API_KEY"])

    # Create or use existing OpenAI assistant
    assistant_id = config.get("OPENAI_ASSISTANT_ID")
    if not assistant_id:
        assistant_id = create_assistant(
            openai_client,
            name="Content Creation Assistant",
            instructions=instructions,
            model="gpt-4-turbo"
        )

    # Load articles CSV
    articles = load_csv_file(config["ARTICLES_CSV"])

    # Parse sitemap for internal links
    sitemap_path = 'path_to_your_sitemap_index.xml'
    internal_links = parse_sitemap(sitemap_path)

    # Upload knowledge profile to OpenAI
    knowledge_profile_id = upload_file(openai_client, config["KNOWLEDGE_PROFILE_JSON"], 'answers')

    # Create a directory for today's date
    today = datetime.today().strftime('%Y-%m-%d')
    articles_dir = os.path.join('articles', today)
    os.makedirs(articles_dir, exist_ok=True)

    # Process each article
    for article in articles:
        slug = article['slug']
        keywords = article['keywords'].split(',')

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
            research_file = os.path.join(articles_dir, f"{slug}_perplexity.md")
            save_markdown_file(research_file, research_content)

            # Upload Perplexity research to OpenAI
            research_file_id = upload_file(openai_client, research_file, 'answers')

            # Generate article using OpenAI assistant
            example_article = load_markdown_file('data/example_article.md')
            article_content = create_article(openai_client, assistant_id,
                                             knowledge_profile_id, research_file_id, example_article, internal_links)

            # Save article to markdown file
            article_file = os.path.join(articles_dir, f"{slug}_Article.md")
            save_markdown_file(article_file, article_content)

            # Convert markdown to HTML
            html_content = convert_markdown_to_html(article_content)

            # Upload article to WordPress if enabled
            if config["UPLOAD_TO_WORDPRESS"]:
                upload_to_wordpress(config["WORDPRESS_USERNAME"], config["WORDPRESS_PASSWORD"],
                                    config["WORDPRESS_API_URL"], f"Article on {', '.join(keywords)}", html_content)

if __name__ == "__main__":
    main()