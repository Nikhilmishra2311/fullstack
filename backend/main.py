from fastapi import FastAPI, HTTPException,Depends 
from fastapi.middleware.cors import CORSMiddleware
from models import product
from database import session, engine 
import database_models
from sqlalchemy.orm import Session


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

database_models.Base.metadata.create_all(bind=engine)

@app.get("/") 
def greet():
    return {"message":"hello everyone"}

products=[
    product(id=1, name="Laptop", description="A high-performance laptop", price=999.99, quantity=10),
    product(id=2, name="Smartphone", description="A latest model smartphone", price=699.99, quantity=25),
    product(id=3, name="Tablet", description="A lightweight tablet", price=399.99, quantity=15),
    product(id=4, name="Headphones", description="Noise-cancelling headphones", price=199.99, quantity=50),
]


def get_db():
    db=session()
    try:
        yield db
    finally:
        db.close()

def init_db():
    db=session()
    count=db.query(database_models.product).count()

    if count==0:
     for product in products:
        db.add(database_models.product(**product.model_dump()))

    db.commit()
init_db()        

@app.get("/products")
def get_products(db:Session=Depends(get_db)):
    db_products=db.query(database_models.product).all()
   

    return db_products

@app.get("/products/{product_id}")
def get_product(id:int, db:Session=Depends(get_db)):
    db_product=db.query(database_models.product).filter(database_models.product.id==id).first()
    if db_product:
        return db_product
    return {"error":"Product not found"}



@app.post("/products")
def add_product(prod:product, db:Session=Depends(get_db)):
    db.add(database_models.product(**prod.model_dump()))
    db.commit()
    return prod

@app.put("/products/{id}")
def update_product(id:int,prod:product, db:Session=Depends(get_db)):
    db_product=db.query(database_models.product).filter(database_models.product.id==id).first()
    if db_product:
            
            db_product.name=prod.name
            db_product.description=prod.description
            db_product.price=prod.price 
            db_product.quantity=prod.quantity
            db.commit()

    else:
         return "Product not found"


@app.delete("/products/{id}")
def delete_product(id:int, db:Session=Depends(get_db)):
    db_product=db.query(database_models.product).filter(database_models.product.id==id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        return " Product deleted successfully"
    return "Product not found"