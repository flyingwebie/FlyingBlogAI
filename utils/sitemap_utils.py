import xml.etree.ElementTree as ET

def parse_sitemap(sitemap_path):
    """
    Parses the sitemap and returns a list of URLs.
    """
    tree = ET.parse(sitemap_path)
    root = tree.getroot()

    # Define the namespaces
    namespaces = {'sitemap': 'http://www.sitemaps.org/schemas/sitemap/0.9'}

    urls = []
    for url in root.findall('sitemap:url', namespaces):
        loc = url.find('sitemap:loc', namespaces).text
        urls.append(loc)

    return urls
