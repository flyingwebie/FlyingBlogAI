import requests
import logging

def perplexity_research(keyword, api_key):
    url = "https://api.perplexity.ai/chat/completions"
    payload = {
        "model": "llama-3-sonar-small-32k-online",
        "messages": [
            {"role": "system", "content": "Be precise and concise."},
            {"role": "user", "content": f"Find highly specific generalised data about {keyword} in 2024. Do not give me any information about specific brands."}
        ]
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {api_key}"
    }

    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        logging.info(f"Perplexity research completed successfully for keyword: {keyword}")
        return response.json()
    else:
        logging.error(f"Perplexity research failed for keyword: {keyword}, status code: {response.status_code}")
        return None
