import logging
from config import load_config, validate_config, validate_files, load_json_file
from openai_client import initialize_openai_client, upload_file, create_article
from perplexity_client import perplexity_research
from file_utils import save_markdown_file, load_csv_file
from wordpress_client import convert_markdown_to_html, upload_to_wordpress

# Initialize logging
logging.basicConfig(level=logging.INFO, filename='app.log', filemode='w',
                    format='%(name)s - %(levelname)s - %(message)s')

def main():
    # Load and validate configuration
    config = load_config()
    if not validate_config(config):
        logging.error("Configuration validation failed. Exiting.")
        return

    if not validate_files(config):
        logging.error("File validation failed. Exiting.")
        return

    # Load knowledge profile JSON
    knowledge_profile = load_json_file(config["KNOWLEDGE_PROFILE_JSON"])

    logging.info("Configuration and files validated successfully.")
    logging.info(f"Knowledge profile loaded: {knowledge_profile}")

    # Initialize OpenAI client
    openai_client = initialize_openai_client(config["OPENAI_API_KEY"])

    # Load articles CSV
    articles = load_csv_file(config["ARTICLES_CSV"])

    # Upload knowledge profile to OpenAI
    knowledge_profile_id = upload_file(openai_client, config["KNOWLEDGE_PROFILE_JSON"], 'answers')

    # Process each article
    for article in articles:
        slug = article['slug']
        keyword = article['keyword']

        # Conduct Perplexity research
        research_result = perplexity_research(keyword, config["PERPLEXITY_API_KEY"])
        if research_result:
            research_file = f"{slug}_perplexity.md"
            save_markdown_file(research_file, str(research_result))

            # Upload Perplexity research to OpenAI
            research_file_id = upload_file(openai_client, research_file, 'answers')

            # Generate article using OpenAI assistant
            example_article = load_markdown_file('example_article.md')
            article_content = create_article(openai_client, config["OPENAI_ASSISTANT_ID"],
                                             knowledge_profile_id, research_file_id, example_article)

            # Save article to markdown file
            article_file = f"{slug}_Article.md"
            save_markdown_file(article_file, article_content)

            # Convert markdown to HTML
            html_content = convert_markdown_to_html(article_content)

            # Upload article to WordPress
            upload_to_wordpress(config["WORDPRESS_USERNAME"], config["WORDPRESS_PASSWORD"],
                                config["WORDPRESS_API_URL"], f"Article on {keyword}", html_content)

if __name__ == "__main__":
    main()
