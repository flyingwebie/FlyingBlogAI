import csv
import os

def load_csv_file(file_path):
    """
    Load a CSV file and return a list of dictionaries.
    Each dictionary represents a row in the CSV file.
    """
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        return list(reader)

def save_markdown_file(file_path, content):
    """
    Save content to a markdown file.
    """
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

def load_markdown_file(file_path):
    """
    Load content from a markdown file.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()
