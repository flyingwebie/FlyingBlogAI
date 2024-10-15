import openai
import fal_client
import asyncio
import os

async def generate_image_fal(client, prompt):
    handler = fal_client.submit(
        "fal-ai/flux/dev",
        arguments={
            "prompt": prompt,
            "model_name": "stabilityai/stable-diffusion-xl-base-1.0",
            "image_size": "square_hd",
        },
    )
    result = handler.get()
    return result.images[0].url

def generate_image_openai(client, prompt):
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="hd",
        n=1,
    )
    return response.data[0].url

def generate_image_sync(client, prompt, provider=None):
    if provider is None:
        provider = os.getenv("IMAGE_PROVIDER", "openai").lower()

    if provider == "openai":
        return generate_image_openai(client, prompt)
    elif provider == "fal":
        return asyncio.run(generate_image_fal(client, prompt))
    else:
        raise ValueError(f"Unsupported image provider: {provider}")
