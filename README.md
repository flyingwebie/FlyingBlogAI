# FlyingBlogAI

FlyingBlogAI is an automated tool designed to streamline the creation of blog posts. This tool utilizes OpenAI's GPT model to generate comprehensive articles based on given keywords and automatically saves them as drafts in WordPress. It also integrates Perplexity AI for conducting research to enhance the quality of the articles.

## Features

- Automates blog post creation using OpenAI's GPT model.
- Conducts research using Perplexity AI to generate relevant content.
- Saves generated articles as drafts in WordPress.
- Supports customization of article sections and content structure.
- Stores articles in a local folder with a structured directory based on the creation date and article slug.

## Prerequisites

- Docker and Docker Compose installed on your machine.
- Python 3.10 or later.
- An OpenAI API key.
- A Perplexity API key.
- WordPress credentials and API URL for uploading drafts.

## Setup

### Using Docker

1. **Clone the repository:**

   ```sh
   git clone https://github.com/yourusername/flyingblogai.git
   cd flyingblogai
   ```

2. **Create and configure your `.env` file:**

   Copy the provided `.env.example` to `.env` and update the values with your own configuration.

   ```sh
   cp .env.example .env
   ```

   Update the `.env` file with your specific details:

   ```env
   # Company Details
   BUSINESS_NAME=your_business_name
   COUNTRY=your_country
   LANGUAGE=your_language

   # OpenAI API key for accessing OpenAI services
   OPENAI_API_KEY=your_openai_api_key
   MODEL=your_openai_model

   # Generate images for articles with DALL-E 3
   GENERATE_IMAGES=true # true or false

   # Perplexity API key for conducting research
   PERPLEXITY_API_KEY=your_perplexity_api_key

   # OpenAI Assistant ID for creating and managing the assistant (OPTIONAL)
   OPENAI_ASSISTANT_ID=your_openai_assistant_id

   # Path to the JSON file containing the company's knowledge profile
   KNOWLEDGE_PROFILE_JSON=data/knowledge_profile.json

   # Path to the CSV file with slugs and keywords for articles
   ARTICLES_CSV=data/articles.csv

   # Flag to control whether to upload articles to WordPress
   UPLOAD_TO_WORDPRESS=false # true or false

   # WordPress credentials and API URL for uploading drafts
   WORDPRESS_USERNAME=your_wordpress_username
   WORDPRESS_PASSWORD=your_wordpress_password
   WORDPRESS_API_URL=https://yourwordpresssite.com/wp-json/wp/v2/posts
   ```

3. **Prepare your data files:**

   - Ensure you have the `knowledge_profile.json` file in the `data` directory.
   - Populate the `articles.csv` with the slugs and keywords for the articles you want to generate.
   - Add the `example_article.md` and `sitemap_index.xml` files in the `data` directory.

4. **Build and run the Docker container:**

   **Dockerfile:**

   ```Dockerfile
   # Use the official Python image from the Docker Hub
   FROM python:3.10-slim

   # Set the working directory in the container
   WORKDIR /app

   # Copy the requirements.txt file into the container
   COPY requirements.txt .

   # Install the required dependencies
   RUN pip install --no-cache-dir -r requirements.txt

   # Copy the rest of the application code into the container
   COPY . .

   # Expose the port the app runs on
   EXPOSE 8000

   # Command to run the application
   CMD ["python", "main.py"]
   ```

   **docker-compose.yaml:**

   ```yaml
   name: flying-blog-ai

   services:
     app:
       build: .
       container_name: MagicDocker
       environment:
         - OPENAI_API_KEY=${OPENAI_API_KEY}
         - MODEL=${MODEL}
         - PERPLEXITY_API_KEY=${PERPLEXITY_API_KEY}
         - OPENAI_ASSISTANT_ID=${OPENAI_ASSISTANT_ID}
         - GENERATE_IMAGES=${GENERATE_IMAGES}
         - KNOWLEDGE_PROFILE_JSON=${KNOWLEDGE_PROFILE_JSON}
         - ARTICLES_CSV=${ARTICLES_CSV}
         - UPLOAD_TO_WORDPRESS=${UPLOAD_TO_WORDPRESS}
         - WORDPRESS_USERNAME=${WORDPRESS_USERNAME}
         - WORDPRESS_PASSWORD=${WORDPRESS_PASSWORD}
         - WORDPRESS_API_URL=${WORDPRESS_API_URL}
         - BUSINESS_NAME=${BUSINESS_NAME}
         - COUNTRY=${COUNTRY}
         - LANGUAGE=${LANGUAGE}
       volumes:
         - .:/app
       command: python main.py
   ```

   Build and start the services:

   ```sh
   docker-compose build
   docker-compose up
   ```

### Using Python Environment

1. **Clone the repository:**

   ```sh
   git clone https://github.com/flyingwebie/FlyingBlogAI.git
   cd flyingblogai
   ```

2. **Create and configure your `.env` file:**

   Copy the provided `.env.example` to `.env` and update the values with your own configuration.

   ```sh
   cp .env.example .env
   ```

   Update the `.env` file with your specific details:

   ```env
   # Company Details
   BUSINESS_NAME=your_business_name
   COUNTRY=your_country
   LANGUAGE=your_language

   # OpenAI API key for accessing OpenAI services
   OPENAI_API_KEY=your_openai_api_key
   MODEL=your_openai_model

   # Generate images for articles with DALL-E 3
   GENERATE_IMAGES=true # true or false

   # Perplexity API key for conducting research
   PERPLEXITY_API_KEY=your_perplexity_api_key

   # OpenAI Assistant ID for creating and managing the assistant (OPTIONAL)
   OPENAI_ASSISTANT_ID=your_openai_assistant_id

   # Path to the JSON file containing the company's knowledge profile
   KNOWLEDGE_PROFILE_JSON=data/knowledge_profile.json

   # Path to the CSV file with slugs and keywords for articles
   ARTICLES_CSV=data/articles.csv

   # Flag to control whether to upload articles to WordPress
   UPLOAD_TO_WORDPRESS=false # true or false

   # WordPress credentials and API URL for uploading drafts
   WORDPRESS_USERNAME=your_wordpress_username
   WORDPRESS_PASSWORD=your_wordpress_password
   WORDPRESS_API_URL=https://yourwordpresssite.com/wp-json/wp/v2/posts
   ```

3. **Prepare your data files:**

   - Ensure you have the `knowledge_profile.json` file in the `data` directory.
   - Populate the `articles.csv` with the slugs and keywords for the articles you want to generate.
   - Add the `example_article.md` and `sitemap_index.xml` files in the `data` directory.

4. **Create and activate a virtual environment:**

   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

5. **Install dependencies:**

   ```sh
   pip install -r requirements.txt
   ```

6. **Run the application:**

   ```sh
   python main.py
   ```

## Usage

Once the application is running, it will automatically start processing the articles listed in `articles.csv`, conducting research using Perplexity AI, generating content using OpenAI, and optionally uploading the drafts to your WordPress site.

### Directory Structure

Generated articles will be stored in a local directory structure as follows:

```
articles/
└── YYYY-MM-DD/
    └── slug-article/
        ├── slug_perplexity.md
        ├── slug_Article.md
        └── slug_Article.html
        └── slug_image.png
```

Where `YYYY-MM-DD` represents the date the article was created, and `slug-article` represents the slug of the article.

## Customization

To customize the structure and content of the generated articles, you can modify the prompts and sections in the `openai_client.py` file.

## Contributing

Feel free to submit issues and pull requests. Contributions are welcome!

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
