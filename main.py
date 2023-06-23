
from fastapi import FastAPI


import requests

import json

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)







@app.get("/")
async def main():
  url="https://harrynull.tech/api/wallpapers/random_anime_wallpaper?download=true"
  r=requests.get(url)
  k=r.json()
  return k
