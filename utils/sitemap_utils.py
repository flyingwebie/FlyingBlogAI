import re
import xml.etree.ElementTree as ET

def parse_sitemap_to_txt(sitemap_path, output_txt_path):
    tree = ET.parse(sitemap_path)
    root = tree.getroot()
    namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}

    links = []
    for url in root.findall('ns:url', namespace):
        loc = url.find('ns:loc', namespace).text
        links.append(loc)

    with open(output_txt_path, 'w') as f:
        for link in links:
            f.write(link + "\n")

def parse_sitemap(sitemap_path):
    """
    Parses the sitemap and returns a list of URLs.
    """
    with open(sitemap_path, 'r') as file:
        content = file.read()
    content = re.sub(r'^\s+', '', content)  # Remove leading whitespace
    tree = ET.parse(sitemap_path)
    root = tree.getroot()

    # Define the namespaces
    namespaces = {'sitemap': 'http://www.sitemaps.org/schemas/sitemap/0.9'}

    urls = []
    for url in root.findall('sitemap:url', namespaces):
        loc = url.find('sitemap:loc', namespaces).text
        urls.append(loc)

    return urls