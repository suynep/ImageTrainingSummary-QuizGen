from urllib.parse import urlparse, parse_qs
from fastapi import FastAPI, Request, Form, Response
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from helpers import validate_link
from uuid import uuid4

app = FastAPI()
SECRET_KEY = "5a04ed44-ca47-4e07-a499-46c8886b618d"  # DON'T EXPOSE IN PROD
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def landing_view(request: Request):

    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/app")
async def app_view(request: Request):
    return templates.TemplateResponse("app_page.html", {"request": request})


@app.get("/app/summary")
async def summary_view(request: Request):
    print(request.session)
    if request.session["embed_link"]:
        return templates.TemplateResponse(
            "summary.html", {"request": request, "link": request.session["embed_link"]}
        )
    else:
        return {"message": "No Link set in the cookie"}


@app.post("/parse")
async def parse_link(request: Request, link: str = Form(...)):
    link = validate_link(link)

    if link != "Error":
        request.session["link"] = link

        # NOTE: The following parsing mechanism currently works ONLY FOR
        #       the video links copied from browser URL, and NOT FOR those
        #       copied using youtube's SHARE feature (path parameter parsing is)
        #       required for this (To Be Done)
        vq = parse_qs(urlparse(link).query).get("v", [""])[0]
        if vq == '':
            vq = urlparse(link).path.lstrip('/') # rudimentary implementation IMPROVE if possible

        request.session["video_id"] = vq
        request.session["embed_link"] = f"https://youtube.com/embed/{vq}"

        response = RedirectResponse(url="/app/summary", status_code=303)
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
