from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def landing_view(request: Request):
    return templates.TemplateResponse(
        "index.html", 
        {"request": request}
    )

@app.get("/app")
async def app_view(request: Request):
    return templates.TemplateResponse(
        "app_page.html", 
        {"request": request}
    )

@app.get("/app/summary")
async def summary_view(request: Request):
    pass

@app.post("/parse")
async def parse_link(request: Request):
    pass