from fastapi import FastAPI
import pymongo
from mongo_baomoi import find_one, find_all
import json

app = FastAPI()

@app.get("/bao_moi/{code}")
async def get_bao_moi(code: str):
    data = find_one(code)
    return {
        "data": data
    }

@app.get("/bao_moi/")
async def get_all(page: int = 1, size: int = 10):
    data = find_all(page, size)
    return {
        "data" : data
    }