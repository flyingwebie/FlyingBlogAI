# FlyingBlogAI

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg) ![Docker](https://img.shields.io/badge/Docker-Supported-brightgreen)

FlyingBlogAI is an automated tool designed to streamline the creation of blog posts. This tool utilizes either OpenAI's GPT model, Anthropic's Claude model, or FAL AI to generate comprehensive articles based on given keywords and automatically saves them as drafts in WordPress. It also integrates Perplexity AI for conducting research to enhance the quality of the articles. The generated articles are enriched with internal links and SEO-friendly content.

## Features

- Generates high-quality blog articles using either OpenAI's GPT-4, Anthropic's Claude, or FAL AI.
- Conducts research using Perplexity API to enhance article content.
- Generates images for articles using DALL-E 3 or FAL AI (optional).
- Handles internal linking using sitemap data.
- Generates sitemaps for better SEO.
- Uploads articles to WordPress (optional).
- Supports multiple AI providers for both text and image generation.
- Asynchronous image generation for improved performance.

## Prerequisites

- Docker and Docker Compose installed on your machine (optional, for containerized deployment).
- Python 3.10 or later.
- API keys for your chosen AI providers (OpenAI, Claude, FAL AI).
- A Perplexity API key.
- WordPress credentials and API URL for uploading drafts (if using WordPress integration).

## Requirements

To run FlyingBlogAI, you will need the following software installed on your system:

- **Python**: Version 3.10 or higher.
- **Docker**: Optional, for containerized deployment.
- **Git**: Optional, for cloning the repository.

## Installation

### Using Docker

1. Build and run the Docker container using Docker Compose:

   ```bash
   docker-compose up
   ```

### Using Python Environment

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/FlyingBlogAI.git
   cd FlyingBlogAI
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

## Configuration

1. Copy `.env.example` to `.env` and update the values with your configuration:

   ```env
   # Company Details
   BUSINESS_NAME=your_business_name
   COUNTRY=your_country
   LANGUAGE=your_language

   # AI Provider Selection (openai, claude, or fal)
   AI_PROVIDER=your_chosen_provider
   IMAGE_PROVIDER=your_chosen_image_provider

   # API Keys
   OPENAI_API_KEY=your_openai_api_key
   CLAUDE_API_KEY=your_claude_api_key
   FAL_API_KEY=your_fal_api_key
   PERPLEXITY_API_KEY=your_perplexity_api_key

   # AI Models
   OPENAI_MODEL=your_openai_model
   CLAUDE_MODEL=your_claude_model

   # OpenAI Assistant ID (OPTIONAL)
   OPENAI_ASSISTANT_ID=your_openai_assistant_id

   # File Paths
   KNOWLEDGE_PROFILE_JSON=data/knowledge_profile.json
   ARTICLES_CSV=data/articles.csv

   # WordPress Configuration
   UPLOAD_TO_WORDPRESS=true
   WORDPRESS_USERNAME=your_wordpress_username
   WORDPRESS_PASSWORD=your_wordpress_password
   WORDPRESS_API_URL=https://yourwordpresssite.com/wp-json/wp/v2
   WORDPRESS_POST_TYPE=your_post_type

   # Image Generation
   GENERATE_IMAGES=true
   ```

## Usage

Once the application is running, it will automatically start processing the articles listed in `articles.csv`, conducting research using Perplexity AI, generating content using the selected AI provider, and optionally uploading the drafts to your WordPress site.

### Running the Main Script

To generate articles and optionally publish them to WordPress:

```bash
python main.py
```

The script will use the AI provider specified in the `AI_PROVIDER` environment variable (either "openai", "claude", or "fal").

### Generating Sitemap

To generate a sitemap from a list of URLs:

```bash
python generate_sitemap.py
```

This script will read the URLs from `data/sitemap_index.txt` and generate `data/sitemap_index.xml`. If the XML file already exists, it will ask for permission to overwrite it.

### Directory Structure

Generated articles will be stored in a local directory structure as follows:

```
articles/
└── YYYY-MM-DD/
    └── slug-article/
        ├── slug_perplexity.md
        ├── slug_Article.md
        └── slug_Article.html
        └── slug_image.png (if GENERATE_IMAGES is true)
```

Where `YYYY-MM-DD` represents the date the article was created, and `slug-article` represents the slug of the article.

## Additional Notes

- Ensure that the `data` directory contains the necessary input files (`knowledge_profile.json`, `articles.csv`, `sitemap_index.txt`).
- The generated articles, images (if enabled), and sitemaps will be stored in the `articles` directory with subdirectories organized by date and slug.
- Make sure to update your `.env` file with correct API keys and configuration details before running the scripts.
- You can switch between OpenAI, Claude, and FAL AI by changing the `AI_PROVIDER` value in the `.env` file.

## Contributing

Feel free to fork the repository and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)
