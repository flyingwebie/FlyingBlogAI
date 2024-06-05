import requests
from config.config import load_config
from bs4 import BeautifulSoup
import os
from clients.wordpress_client import upload_image_to_wordpress, upload_to_wordpress

def upload_articles_in_directory(articles_dir):
    """
    Upload articles in the specified directory to WordPress and move them to the 'uploaded' folder upon success.
    """
    config = load_config()

    if not os.path.exists(articles_dir) or not os.listdir(articles_dir):
        print("No articles found in the directory.")
        return

    uploaded_dir = os.path.join('uploaded')
    os.makedirs(uploaded_dir, exist_ok=True)

    for root, _, files in os.walk(articles_dir):
        for file in files:
            if file.endswith('_Article.html'):
                article_path = os.path.join(root, file)
                article_slug = os.path.basename(root)

                print(f"Processing article: {article_path}")

                # Read the article content
                with open(article_path, 'r', encoding='utf-8') as f:
                    article_content = f.read()

                # Extract the title from the first line of the HTML content
                soup = BeautifulSoup(article_content, 'html.parser')
                title_tag = soup.find('h1')
                title = title_tag.get_text() if title_tag else f"Article on {article_slug}"

                # Upload feature image to WordPress if GENERATE_IMAGES is true and image exists
                image_path = os.path.join(root, f"{article_slug}_image.png")
                featured_image_id = None
                generate_images = str(config.get("GENERATE_IMAGES", "false")).lower()
                if generate_images == "true" and os.path.exists(image_path):
                    try:
                        featured_image_id = upload_image_to_wordpress(
                            config["WORDPRESS_USERNAME"],
                            config["WORDPRESS_PASSWORD"],
                            config["WORDPRESS_API_URL"],
                            image_path
                        )
                    except requests.exceptions.RequestException as e:
                        print(f"Failed to upload image '{image_path}': {e}")
                        continue  # Skip to the next article

                # Encode the article content to ensure proper character display
                article_content_encoded = article_content.encode('utf-8').decode('latin-1')

                # Upload article to WordPress
                try:
                    upload_to_wordpress(
                        config["WORDPRESS_USERNAME"],
                        config["WORDPRESS_PASSWORD"],
                        config["WORDPRESS_API_URL"],
                        title,
                        article_content_encoded,
                        featured_image_id,
                        post_type=config.get("WORDPRESS_POST_TYPE", "posts"),
                        slug=article_slug
                    )

                    # Move the article folder to 'uploaded' directory upon success
                    destination_dir = os.path.join(uploaded_dir, os.path.basename(root))
                    os.rename(root, destination_dir)
                    print(f"Article '{title}' uploaded successfully and moved to '{destination_dir}'.")

                except requests.exceptions.RequestException as e:
                    print(f"Failed to upload article '{title}': {e}")

if __name__ == "__main__":
    articles_dir = "articles"
    upload_articles_in_directory(articles_dir)
