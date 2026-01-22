from fastapi import Depends, FastAPI, HTTPException
from .database import SessionLocal, engine
from . import schemas, models
from sqlalchemy.orm import Session
from . import crud
from fastapi.security import OAuth2PasswordRequestForm
from .auth import verify_password, create_access_token, get_current_user


models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Jewerly CRM")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post('/items/', response_model=schemas.Item)
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_item = crud.get_item_by_article(db, article=item.article)
    if db_item:
        raise HTTPException(status_code=400, detail="Артикул уже существует")
    return crud.create_item(db=db, item=item)

@app.get('/items/', response_model = list[schemas.Item])
def read_items(skip: int=0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items

@app.get("/customers/", response_model=list[schemas.Customer])
def read_customers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return crud.get_customers(db, skip=skip, limit=limit)

@app.post("/customers", response_model=schemas.Customer)
def create_customer(customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    db_customer = crud.get_customer_by_phone(db, phone = customer.phone)
    if db_customer:
        raise HTTPException(status_code=400, detail='Клиент с таким телефоном уже зарегистрирован')
    return crud.create_customer(db=db, customer=customer)

@app.post("/orders/", response_model=schemas.Order)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    db_item = crud.get_item_by_id(db, item_id=order.item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Товар не найден")
    
    db_customer = crud.get_customer_by_id(db, id=order.customer_id)
    if not db_customer:
        raise HTTPException(status_code=404, detail="Клиент не найден")
    
    return crud.create_order(db=db, order=order)

@app.get("/orders/", response_model=list[schemas.Order])
def read_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_orders(db, skip=skip, limit=limit)

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user=user)

@app.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Неверное имя пользователя или пароль",
            headers={"WWW-Authenticate": "Bearer"}
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

