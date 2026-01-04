from fastapi import FastAPI
from stars import router as stars_data
from planets import router as planets_data
import requests,json

app = FastAPI()

app.include_router(stars_data)
app.include_router(planets_data)
