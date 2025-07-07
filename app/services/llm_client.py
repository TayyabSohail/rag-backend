from dotenv import load_dotenv
load_dotenv()

import httpx
import os

MISTRAL_API_KEY = os.getenv("LLM_API_KEY")
BASE_URL = "https://api.mistral.ai/v1/chat/completions"

async def query_llm(prompt: str):
    print("🔑 MISTRAL_API_KEY:", MISTRAL_API_KEY)  # Debug: Make sure the key is loaded

    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json"
    }

    body = {
        "model": "mistral-small-latest",  # You can change to mistral-medium or mistral-large
        "messages": [
            {"role": "system", "content": "You're a helpful assistant answering using context."},
            {"role": "user", "content": prompt}
        ]
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(BASE_URL, json=body, headers=headers)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
