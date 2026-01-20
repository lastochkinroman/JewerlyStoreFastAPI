from fastapi import FastAPI
from . import models
from .database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Jewerly CRM")

@app.get("/")
def read_root():
    return {"message": "CRM система ювелирного магазина готова к работе"}