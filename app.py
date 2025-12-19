from datetime import date
from fastapi import FastAPI, Depends, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from db import SessionLocal, engine
from models import Base
from queries import general_metrics, revenue_timeseries, list_venues, list_sports

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Sportomic Metrics API")
templates = Jinja2Templates(directory="templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {
        "service": "Sportomic Metrics API",
        "docs": "/docs",
        "dashboard": "/dashboard",
        "endpoints": [
            "/venues",
            "/sports",
            "/metrics/general",
            "/metrics/revenue_timeseries",
        ],
    }

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/metrics/general")
def get_general_metrics(
    start_date: date | None = Query(default=None),
    end_date: date | None = Query(default=None),
    venue_id: int | None = Query(default=None),
    sport_id: int | None = Query(default=None),
    db: Session = Depends(get_db),
):
    return general_metrics(db, start_date, end_date, venue_id, sport_id)

@app.get("/metrics/revenue_timeseries")
def get_revenue_timeseries(
    start_date: date | None = Query(default=None),
    end_date: date | None = Query(default=None),
    venue_id: int | None = Query(default=None),
    sport_id: int | None = Query(default=None),
    db: Session = Depends(get_db),
):
    return revenue_timeseries(db, start_date, end_date, venue_id, sport_id)

@app.get("/venues")
def get_venues(db: Session = Depends(get_db)):
    return list_venues(db)

@app.get("/sports")
def get_sports(db: Session = Depends(get_db)):
    return list_sports(db)

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(req: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse("dashboard.html", {"request": req})
