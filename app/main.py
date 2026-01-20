from fastapi import FastAPI

app = FastAPI(title="Jewerly CRM")

@app.get("/")
def read_root():
    return {"message": "CRM система ювелирного магазина готова к работе"}