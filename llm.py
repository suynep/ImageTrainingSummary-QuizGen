import os
import json
from dotenv import load_dotenv
from google import genai
from google.genai import types
from youtube_transcript_api import YouTubeTranscriptApi

load_dotenv()

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
MODEL = "gemini-2.0-flash"

with open('prompt.txt', 'r') as f:
    global PROMPT
    PROMPT = f.read()

client = genai.Client(api_key=GEMINI_API_KEY)

ytt_api = YouTubeTranscriptApi()

def fetch_transcript_text(video_id: str):
    fetched = ytt_api.fetch(video_id)
    data = []
    for snippet in fetched:
        data.append({"text": snippet.text, "start": snippet.start, "duration": snippet.duration})

    return json.dumps(data)

def generate_custom_json(data: str):
    """
    :param: data - youtube transcript data (run after fetching from fetch_transcript_text()) 
    """
    response = client.models.generate_content(
        model=MODEL,
        contents=PROMPT + data,
        config=types.GenerateContentConfig(
            response_mime_type="application/json"
        ),
    )
    return response.model_dump_json()