from dotenv import load_dotenv
load_dotenv()

import httpx
import os

MISTRAL_API_KEY = os.getenv("LLM_API_KEY")
BASE_URL = "https://api.mistral.ai/v1/chat/completions"

async def query_llm(messages: list[dict]):
    print("🔐 Using Mistral API Key:", bool(MISTRAL_API_KEY))  # For debug

    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json"
    }

    body = {
        "model": "mistral-small-latest",  # or mistral-medium-latest
        "messages": messages
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(BASE_URL, json=body, headers=headers)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
