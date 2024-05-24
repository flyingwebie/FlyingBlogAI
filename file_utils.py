def save_markdown_file(file_path, content):
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
        logging.info(f"Saved markdown file: {file_path}")
