import os
from dotenv import load_dotenv
from openai import OpenAI
import fal_client
import asyncio
from clients.image_utils import generate_image_openai, generate_image_fal
import requests

# Load environment variables
load_dotenv()

# Get the image provider from environment variables
image_provider = os.getenv("IMAGE_PROVIDER", "openai").lower()

# Initialize clients
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
fal_client.api_key = os.getenv("FAL_API_KEY")

def download_image(url, file_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(file_path, 'wb') as file:
            file.write(response.content)
        print(f"Image saved to: {file_path}")
    else:
        print(f"Failed to download image. Status code: {response.status_code}")

async def main():
    # Test prompt
    prompt = input("Enter the image prompt: ")

    # Ask for custom filename
    custom_filename = input("Enter a custom filename (leave blank for default): ")

    try:
        if image_provider == "fal":
            image_url = await generate_image_fal(fal_client, prompt)
        elif image_provider == "openai":
            image_url = generate_image_openai(openai_client, prompt)
        else:
            raise ValueError(f"Unsupported image provider: {image_provider}")

        print(f"Image generated successfully using {image_provider.upper()}!")
        print(f"Image URL: {image_url}")

        # Create 'images' folder if it doesn't exist
        if not os.path.exists('images'):
            os.makedirs('images')

        # Download and save the image
        if custom_filename:
            image_filename = f"{custom_filename}.png"
        else:
            image_filename = f"generated_image_{image_provider}.png"
        image_path = os.path.join('images', image_filename)
        download_image(image_url, image_path)

    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())
