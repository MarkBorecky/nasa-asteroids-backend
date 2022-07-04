from datetime import date
from fastapi.middleware.cors import CORSMiddleware

from fastapi import FastAPI
from models import DateRange
import asteroid_servise

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/v1/asteroids")
async def fetch_asteroids(start_date: date, end_date: date):
    return asteroid_servise.fetch_asteroids_between(DateRange(start_date, end_date))
