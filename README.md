# Automated Blog Post Creation and Draft Saving Tool

## Project Description

This project is a Python-based tool designed to automate the creation of blog posts using AI-driven research and content generation. It integrates with OpenAI and Perplexity APIs to gather information and create articles, which are then saved as drafts in a WordPress website. The tool ensures efficient and high-quality content creation, leveraging pre-defined knowledge profiles and example articles for consistency.

## Features

- Automates research and article creation based on provided keywords.
- Uses Perplexity API for gathering relevant data.
- Utilizes OpenAI's GPT-4 for generating well-structured articles.
- Converts markdown articles to HTML.
- Uploads and saves articles as drafts in a WordPress site.
- Validates configuration and input files before processing.
- Logs errors and processes for debugging purposes.

## Setup and Usage

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Access to OpenAI API
- Access to Perplexity API
- WordPress account with API access

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/your-repo.git
   cd your-repo
   ```

2. **Create a virtual environment**

   ```bash
   python -m venv env
   ```

3. **Activate the virtual environment**

   - On Windows:
     ```bash
     .\env\Scripts\activate
     ```
   - On macOS and Linux:
     ```bash
     source env/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Configuration

1. **Create a `.env` file** in the root directory and add the following configurations:

   ```ini
   OPENAI_API_KEY=your_openai_api_key
   PERPLEXITY_API_KEY=your_perplexity_api_key
   OPENAI_ASSISTANT_ID=your_openai_assistant_id
   KNOWLEDGE_PROFILE_JSON=knowledge_profile.json
   ARTICLES_CSV=articles.csv
   WORDPRESS_USERNAME=your_wordpress_username
   WORDPRESS_PASSWORD=your_wordpress_password
   WORDPRESS_API_URL=https://yourwordpresssite.com/wp-json/wp/v2/posts
   ```

2. **Prepare the input files**:
   - `knowledge_profile.json`: JSON file containing your company's knowledge profile.
   - `articles.csv`: CSV file with columns `slug` and `keyword` for each article to be created.
   - `example_article.md`: Markdown file that serves as an example article for structure and tone.

### Running the Application

1. **Ensure the virtual environment is activated**:

   ```bash
   source env/bin/activate  # For macOS/Linux
   .\env\Scripts\activate  # For Windows
   ```

2. **Run the main script**:
   ```bash
   python main.py
   ```

### Logging and Debugging

- The application logs all processes and errors to `app.log` file in the root directory.
- Check this log file for detailed information if anything goes wrong.

### Example File Formats

**articles.csv**

```csv
slug,keyword
example-slug-1,example keyword 1
example-slug-2,example keyword 2
```
