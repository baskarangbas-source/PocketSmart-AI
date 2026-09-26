from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="PocketSmart AI")
templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")


def make_recommendations(category: str, budget: float, preference: str):
    plans = {
        "Home Interior": [
            ("Furniture", 0.35),
            ("Lighting", 0.15),
            ("Decor", 0.15),
            ("Storage", 0.20),
            ("Contingency", 0.15),
        ],
        "Party Planning": [
            ("Venue", 0.30),
            ("Food & Drinks", 0.30),
            ("Decoration", 0.15),
            ("Entertainment", 0.15),
            ("Contingency", 0.10),
        ],
        "Jewelry Planning": [
            ("Main Purchase", 0.55),
            ("Customization", 0.15),
            ("Accessories", 0.10),
            ("Savings Buffer", 0.20),
        ],
    }

    preference = preference.lower().strip()

    if category == "Home Interior":
        if preference == "modern":
            plans[category] = [
                ("Furniture", 0.40),
                ("Lighting", 0.20),
                ("Decor", 0.20),
                ("Storage", 0.10),
                ("Contingency", 0.10),
            ]
        elif preference == "simple":
            plans[category] = [
                ("Furniture", 0.30),
                ("Lighting", 0.15),
                ("Decor", 0.10),
                ("Storage", 0.25),
                ("Contingency", 0.20),
            ]
        elif preference == "premium":
            plans[category] = [
                ("Furniture", 0.50),
                ("Lighting", 0.20),
                ("Decor", 0.15),
                ("Storage", 0.10),
                ("Contingency", 0.05),
            ]

    selected_plan = plans.get(category, plans["Home Interior"])

    return [
        {"name": name, "amount": round(budget * percentage, 2)}
        for name, percentage in selected_plan
    ]


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
            "recommendations": make_recommendations(category, budget, preference),
            "category": category,
            "budget": budget,
            "preference": preference,
        },
    )


@app.get("/health")
async def health():
    return {"status": "ok"}
