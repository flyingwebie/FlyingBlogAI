import os

def generate_sitemap(input_file, output_file):
    # Check if the input file exists
    if not os.path.exists(input_file):
        print(f"Input file {input_file} does not exist.")
        return

    # Check if the output file already exists
    if os.path.exists(output_file):
        overwrite = input(f"The file {output_file} already exists. Do you want to overwrite it? (y/N): ")
        if overwrite.lower() != 'y':
            print("Operation cancelled. The sitemap was not generated.")
            return

    # Read URLs from the input file
    with open(input_file, 'r') as file:
        urls = [line.strip() for line in file if line.strip()]

    # Create the XML content
    xml_content = '''<?xml version="1.0" encoding="UTF-8"?><?xml-stylesheet type="text/xsl" href="//www.flyingweb.ie/main-sitemap.xsl"?>
<urlset xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1" xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd http://www.google.com/schemas/sitemap-image/1.1 http://www.google.com/schemas/sitemap-image/1.1/sitemap-image.xsd" xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
'''
    for url in urls:
        xml_content += f'''    <url>
        <loc>{url}</loc>
    </url>
'''
    xml_content += '</urlset>'

    # Write the XML content to the output file
    with open(output_file, 'w') as file:
        file.write(xml_content)

    print(f"Sitemap generated successfully: {output_file}")

if __name__ == "__main__":
    input_file = 'data/sitemap_index.txt'
    output_file = 'data/sitemap_index.xml'
    generate_sitemap(input_file, output_file)
