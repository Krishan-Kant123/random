
from fastapi import FastAPI


import requests

import json

from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware





middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*']
    )
]

app = FastAPI(middleware=middleware)






@app.get("/")
async def main():
  url="https://harrynull.tech/api/wallpapers/random_anime_wallpaper?download=true"
  r=requests.get(url)
  k=r.json()
  return k
