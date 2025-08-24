import os
import json
import asyncio
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from google import genai
from google.genai import types
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.proxies import WebshareProxyConfig

load_dotenv()

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
MODEL = "gemini-2.0-flash"

with open('prompt.txt', 'r') as f:
    PROMPT = f.read()

client = genai.Client(api_key=GEMINI_API_KEY)
ytt_api = YouTubeTranscriptApi(
    # The following credentials are tied to my WebShare Account (WILL BE REMOVED POST-HACKATHON)
    proxy_config=WebshareProxyConfig(
        proxy_username="mfrlnouc",
        proxy_password="6hvumoogmmj0",
    )
)

templates = Jinja2Templates(directory="templates")

# ---------------------
# Worker Functions
# ---------------------

def _fetch_transcript_text(video_id: str) -> str:
    """Blocking transcript fetch, offloaded to thread in async context."""
    fetched = ytt_api.fetch(video_id)
    data = []
    for snippet in fetched:
        data.append({"text": snippet.text, "start": snippet.start, "duration": snippet.duration})

    return json.dumps(data)

def _generate_custom_json(data: str) -> str:
    """Blocking Gemini call, offloaded to thread in async context."""
    response = client.models.generate_content(
        model=MODEL,
        contents=PROMPT + data,
        config=types.GenerateContentConfig(
            response_mime_type="application/json"
        ),
    )
    return response.model_dump_json()


# ---------------------
# Async wrappers
# ---------------------

async def fetch_transcript_text(video_id: str) -> str:
    return await asyncio.to_thread(_fetch_transcript_text, video_id)

async def generate_custom_json(data: str) -> str:
    return await asyncio.to_thread(_generate_custom_json, data)

