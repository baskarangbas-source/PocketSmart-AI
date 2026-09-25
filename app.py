from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="PocketSmart AI")
templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")


def make_recommendations(category: str, budget: float):
    plans = {
        "Home Interior": [
            ("Furniture", 0.35), ("Lighting", 0.15),
            ("Decor", 0.15), ("Storage", 0.20), ("Contingency", 0.15)
        ],
        "Party Planning": [
            ("Venue", 0.30), ("Food & Drinks", 0.30),
            ("Decoration", 0.15), ("Entertainment", 0.15), ("Contingency", 0.10)
        ],
        "Jewelry Planning": [
            ("Main Purchase", 0.55), ("Customization", 0.15),
            ("Accessories", 0.10), ("Savings Buffer", 0.20)
        ],
    }
    return [{"name": n, "amount": round(budget * p, 2)}
            for n, p in plans.get(category, plans["Home Interior"])]


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "recommendations": []}
    )


@app.post("/recommend", response_class=HTMLResponse)
async def recommend(request: Request):
    form = await request.form()
    category = str(form.get("category", "Home Interior"))
    budget = float(form.get("budget", 0))
    preference = str(form.get("preference", ""))

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "recommendations": make_recommendations(category, budget),
            "category": category,
            "budget": budget,
            "preference": preference,
        },
    )


@app.get("/health")
async def health():
    return {"status": "ok"}
