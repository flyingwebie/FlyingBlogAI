import openai
import fal_client

async def generate_image(client, prompt, provider="openai"):
    if provider == "openai":
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="hd",
            n=1,
        )
        image_url = response.data[0].url
    elif provider == "fal":
        # Use the FAL.AI client to submit a request
        handler = fal_client.submit(
            "fal-ai/flux/dev",
            arguments={
                "prompt": prompt,
                "model_name": "stabilityai/stable-diffusion-xl-base-1.0",
                "image_size": "square_hd",
            },
        )
        result = handler.get()
        image_url = result.images[0].url
    else:
        raise ValueError(f"Unsupported image provider: {provider}")

    return image_url
