from fastapi import Depends, FastAPI, HTTPException
from .database import SessionLocal, engine
from . import schemas, models
from sqlalchemy.orm import Session
from . import crud

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Jewerly CRM")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post('/items/', response_model=schemas.Item)
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    db_item = crud.get_item_by_article(db, article=item.article)
    if db_item:
        raise HTTPException(status_code=400, detail="Артикул уже существует")
    return crud.create_item(db=db, item=item)

@app.get('/items/', response_model = list[schemas.Item])
def read_items(skip: int=0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items

@app.get("/customers/", response_model=list[schemas.Customer])
def read_customers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_customers(db, skip=skip, limit=limit)

@app.post("/customers", response_model=schemas.Customer)
def create_customer(customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    db_customer = crud.get_customer_by_phone(db, phone = customer.phone)
    if db_customer:
        raise HTTPException(status_code=400, detail='Клиент с таким телефоном уже зарегистрирован')
    return crud.create_customer(db=db, customer=customer)