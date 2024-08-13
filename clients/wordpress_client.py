import os
import requests
import markdown2
import logging
import base64
import mimetypes

def convert_markdown_to_html(markdown_content):
    """
    Convert markdown content to HTML, including tables.
    https://github.com/trentm/python-markdown2/wiki/Extras
    """
    html_content = markdown2.markdown(markdown_content, extras=["tables", "fenced-code-blocks", "strike", "code-friendly", "header-ids", "cuddled-lists" ])
    return html_content

def save_html_file(file_path, html_content):
    """
    Save HTML content to a file.
    """
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(html_content)

def upload_image_to_wordpress(username, password, api_url, image_path):
    with open(image_path, 'rb') as img:
        image_data = img.read()

    credentials = f"{username}:{password}"
    token = base64.b64encode(credentials.encode())

    # Determine the MIME type based on the image file extension
    mime_type, _ = mimetypes.guess_type(image_path)
    if not mime_type:
        mime_type = 'application/octet-stream'

    headers = {
        'Authorization': f'Basic {token.decode("utf-8")}',
        'Content-Disposition': f'attachment; filename={os.path.basename(image_path)}',
        'Content-Type': mime_type
    }

    response = requests.post(f"{api_url}/media", headers=headers, data=image_data)

    if response.status_code == 201:
        print(f"Image '{os.path.basename(image_path)}' uploaded successfully.")
        return response.json()['id']
    else:
        print(f"Failed to upload image '{os.path.basename(image_path)}': {response.status_code} - {response.text}")
        response.raise_for_status()

def upload_to_wordpress(username, password, api_url, title, content, featured_image_id=None, post_type="posts", slug=None):
    credentials = f"{username}:{password}"
    token = base64.b64encode(credentials.encode())
    headers = {
        'Authorization': f'Basic {token.decode("utf-8")}',
        'Content-Type': 'application/json'
    }

    post_data = {
        'title': title,
        'content': content,
        'status': 'draft',
        'slug': slug,
        'type': post_type,
        'parent': '46'
    }

    if featured_image_id:
        post_data['featured_media'] = featured_image_id

    response = requests.post(f"{api_url}/{post_type}", headers=headers, json=post_data)
    response.raise_for_status()
    return response.json()