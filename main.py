# This file is a biryani ahile and I'm too lazy to refactor 🥲🥲

import json
from db import insert_one_to_db, find_data_by_id, get_all
from urllib.parse import urlparse, parse_qs
from fastapi import FastAPI, Request, Form, Response
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from helpers import validate_link
from llm import generate_custom_json, fetch_transcript_text
from uuid import uuid4
import markdown
from pdf_generator import generate_quiz_pdf

app = FastAPI()
SECRET_KEY = "5a04ed44-ca47-4e07-a499-46c8886b618d"  # Change in prod
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def landing_view(request: Request):

    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/app")
async def app_view(request: Request):
    return templates.TemplateResponse("app_page.html", {"request": request})


@app.get("/summary-page")
async def summary_page(request: Request):
    """Serves HTML immediately"""
    return templates.TemplateResponse("summary.html", {"request": request})

# 👇👇👇👇👇👇 YO IMPLEMENT PACHIIIIII!!!!! (if needed lol)
# @app.get("/community")
# async def community_view(request: Request):
#     return templates.TemplateResponse("community.html", {"request": request})    "question": "string",
    # "answer_choices": ["string", "string", "string", "string"],
    # "answer": "string",
    # "timestamp": [float, float],  // start times in seconds

# @app.get("/api/all-community-posts")
# async def community_data(request: Request):
#     posts = get_all()
#     return {"posts": posts}


@app.get("/app/summary-data")
async def summary_data(request: Request):
    embed_link = request.session.get("embed_link")
    video_id = request.session.get("video_id")
    if not embed_link or not video_id:
        return {"message": "No Link set in the cookie"}

    res = find_data_by_id(video_id) # check if the video has already been LLM-ized and is stored in the MongoDB

    if not res:
        transcript_json = await fetch_transcript_text(video_id)
        llm_res = await generate_custom_json(transcript_json)
        llm_res = json.loads(llm_res)

        questions = json.loads(llm_res['candidates'][0]['content']['parts'][0]['text'])['questions']
        summary = json.loads(llm_res['candidates'][0]['content']['parts'][0]['text'])['summary']
        flashcards = json.loads(llm_res['candidates'][0]['content']['parts'][0]['text'])['flashcards']

        insert_one_to_db({"embed_link": embed_link, "questions": questions, "summary": summary, "_id": video_id, "flashcards": flashcards})

        generate_quiz_pdf(questions)


        # Return JSON instead of HTML
        print(markdown.markdown(summary))
        return {"embed_link": embed_link, "questions": questions, "summary": markdown.markdown(summary), "flashcards": flashcards}
    else:
        data = {
            "embed_link": res['embed_link'], 
            "questions": res['questions'], 
            "summary": markdown.markdown(res['summary']), 
            "_id": res['_id'],
            "flashcards": res['flashcards'],
        }

        print(data['questions'])
        generate_quiz_pdf(data['questions'])
        return data 


@app.post("/parse")
async def parse_link(request: Request, link: str = Form(...)):
    link = validate_link(link)

    if link != "Error":
        request.session["link"] = link

        # NOTE: The following parsing mechanism currently works ONLY FOR
        #       the video links copied from browser URL, and NOT FOR those
        #       copied using youtube's SHARE feature (path parameter parsing is
        #       required for this) (To Be Done)
        vq = parse_qs(urlparse(link).query).get("v", [""])[0]
        if vq == '':
            vq = urlparse(link).path.lstrip('/') # rudimentary implementation; IMPROVE if possible

        request.session["video_id"] = vq
        request.session["embed_link"] = f"https://youtube.com/embed/{vq}"

        response = RedirectResponse(url="/summary-page", status_code=303)
        response.set_cookie(
            key="video_id",
            value=vq,
            secure=True,
            httponly=False,
        )

        response.set_cookie(
            key="link",
            value=link,
            secure=True,
            httponly=False,
        )

        response.set_cookie(
            key="embed_link",
            value=f"https://youtube.com/embed/{vq}",
            secure=True,
            httponly=False,
        )

        return response
    else:
        return {"error": "Invalid link provided"}