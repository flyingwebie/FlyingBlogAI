# FlyingBlogAI

FlyingBlogAI is an automated tool designed to streamline the creation of blog posts. This tool utilizes either OpenAI's GPT model or Anthropic's Claude model to generate comprehensive articles based on given keywords and automatically saves them as drafts in WordPress. It also integrates Perplexity AI for conducting research to enhance the quality of the articles. The generated articles are enriched with internal links and SEO-friendly content.

## Features

- Generates high-quality blog articles using either OpenAI's GPT-4 or Anthropic's Claude.
- Conducts research using Perplexity API.
- Generates images for articles using DALL-E 3 (optional).
- Handles internal linking using sitemap data.
- Generates sitemaps for better SEO.
- Uploads articles to WordPress (optional).

## Prerequisites

- Docker and Docker Compose installed on your machine.
- Python 3.10 or later.
- An OpenAI API key or Claude API key (depending on your chosen AI provider).
- A Perplexity API key.
- WordPress credentials and API URL for uploading drafts (if using WordPress integration).

## Requirements

To run FlyingBlogAI, you will need the following software installed on your system:

- **Python**: Version 3.9 or higher. Python is a programming language required to run the scripts.
- **Docker**: Optional. Docker is used to containerize the application, making it easier to run without worrying about the environment setup.
- **Git**: Optional. Git is a version control system used to clone the repository. You can also download the repository as a ZIP file if you prefer.

If you don't have these installed, here are some resources to help you get started:

- [Download Python](https://www.python.org/downloads/)
- [Download Docker](https://www.docker.com/get-started)
- [Download Git](https://git-scm.com/downloads)

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

   # AI Provider Selection (openai or claude)
   AI_PROVIDER=your_chosen_provider

   # OpenAI API key for accessing OpenAI services
   OPENAI_API_KEY=your_openai_api_key
   OPENAI_MODEL=your_openai_model

   # Claude API key and model
   CLAUDE_API_KEY=your_claude_api_key
   CLAUDE_MODEL=your_claude_model

   # Perplexity API key for conducting research
   PERPLEXITY_API_KEY=your_perplexity_api_key

   # OpenAI Assistant ID for creating and managing the assistant (OPTIONAL)
   OPENAI_ASSISTANT_ID=your_openai_assistant_id

   # Path to the JSON file containing the company's knowledge profile
   KNOWLEDGE_PROFILE_JSON=data/knowledge_profile.json

   # Path to the CSV file with slugs and keywords for articles
   ARTICLES_CSV=data/articles.csv

   # Flag to control whether to upload articles to WordPress
   UPLOAD_TO_WORDPRESS=true # true or false

   # WordPress credentials and API URL for uploading drafts
   WORDPRESS_USERNAME=your_wordpress_username
   WORDPRESS_PASSWORD=your_wordpress_password
   WORDPRESS_API_URL=https://yourwordpresssite.com/wp-json/wp/v2
   WORDPRESS_POST_TYPE=your_post_type

   # Generate images for articles with DALL-E 3
   GENERATE_IMAGES=true # true or false
   ```

## Usage

Once the application is running, it will automatically start processing the articles listed in `articles.csv`, conducting research using Perplexity AI, generating content using the selected AI provider (OpenAI or Claude), and optionally uploading the drafts to your WordPress site.

### Running the Main Script

To generate articles and optionally publish them to WordPress:

```bash
python main.py
```

The script will use the AI provider specified in the `AI_PROVIDER` environment variable (either "openai" or "claude").

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
- You can switch between OpenAI and Claude by changing the `AI_PROVIDER` value in the `.env` file.

## Contributing

Feel free to fork the repository and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)
