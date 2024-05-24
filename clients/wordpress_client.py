import requests
import markdown
import logging

def convert_markdown_to_html(markdown_content):
    html_content = markdown.markdown(markdown_content)
    logging.info("Converted markdown to HTML.")
    return html_content

def upload_to_wordpress(username, password, api_url, article_title, article_content):
    data = {
        'title': article_title,
        'content': article_content,
        'status': 'draft'
    }
    response = requests.post(api_url, auth=(username, password), json=data)
    if response.status_code == 201:
        logging.info("Article uploaded to WordPress successfully.")
    else:
        logging.error(f"Failed to upload article to WordPress: {response.status_code}, {response.text}")
