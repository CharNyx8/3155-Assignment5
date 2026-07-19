from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

from .models import models, schemas
from .controllers import orders, sandwiches, resources, recipes, order_details
from .dependencies.database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/orders/", response_model=schemas.Order, tags=["Orders"])
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    return orders.create(db=db, order=order)


@app.get("/orders/", response_model=list[schemas.Order], tags=["Orders"])
def read_orders(db: Session = Depends(get_db)):
    return orders.read_all(db)


@app.get("/orders/{order_id}", response_model=schemas.Order, tags=["Orders"])
def read_one_order(order_id: int, db: Session = Depends(get_db)):
    order = orders.read_one(db, order_id=order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="User not found")
    return order


@app.put("/orders/{order_id}", response_model=schemas.Order, tags=["Orders"])
def update_one_order(order_id: int, order: schemas.OrderUpdate, db: Session = Depends(get_db)):
    order_db = orders.read_one(db, order_id=order_id)
    if order_db is None:
        raise HTTPException(status_code=404, detail="User not found")
    return orders.update(db=db, order=order, order_id=order_id)


@app.delete("/orders/{order_id}", tags=["Orders"])
def delete_one_order(order_id: int, db: Session = Depends(get_db)):
    order = orders.read_one(db, order_id=order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="User not found")
    return orders.delete(db=db, order_id=order_id)

# Sandwiches

@app.post("/sandwiches", tags=["Sandwiches"])
def create_sandwich(request: schemas.SandwichCreate, db: Session = Depends(get_db)):
    return sandwiches.create(db, request)

@app.get("/sandwiches", tags=["Sandwiches"])
def read_sandwiches(db: Session = Depends(get_db)):
    return sandwiches.read_all(db)

@app.get("/sandwiches/{sandwich_id}", tags=["Sandwiches"])
def read_sandwich(sandwich_id: int, db: Session = Depends(get_db)):
    return sandwiches.read_one(db, sandwich_id)

@app.put("/sandwiches/{sandwich_id}", tags=["Sandwiches"])
def update_sandwich(sandwich_id: int, request: schemas.SandwichUpdate, db: Session = Depends(get_db)):
    return sandwiches.update(db, sandwich_id, request)

@app.delete("/sandwiches/{sandwich_id}", tags=["Sandwiches"])
def delete_sandwich(sandwich_id: int, db: Session = Depends(get_db)):
    sandwiches.delete(db, sandwich_id)

# Resources

@app.post("/resources", tags=["Resources"])
def create_resources(request: schemas.ResourceCreate, db: Session = Depends(get_db)):
    return resources.create(db, request)

@app.get("/resources", tags=["Resources"])
def read_resources(db: Session = Depends(get_db)):
    return resources.read_all(db)

@app.get("/resources/{resource_id}", tags=["Resources"])
def read_resource(resource_id: int, db: Session = Depends(get_db)):
    return resources.read_one(db, resource_id)

@app.put("/resources/{resource_id}", tags=["Resources"])
def update_resource(resource_id: int, request: schemas.ResourceUpdate, db: Session = Depends(get_db)):
    return resources.update(db, resource_id, request)

@app.delete("/resources/{resource_id}", tags=["Resources"])
def delete_resource(resource_id: int, db: Session = Depends(get_db)):
    resources.delete(db, resource_id)

#Recipes
@app.post("/recipes", tags=["Recipes"])
def create_recipe(request: schemas.RecipeCreate, db: Session = Depends(get_db)):
    return recipes.create(db, request)

@app.get("/recipes", tags=["Recipes"])
def read_recipes(db: Session = Depends(get_db)):
    return recipes.read_all(db)

@app.get("/recipes/{recipes_id}", tags=["Recipes"])
def read_recipe(recipes_id: int, db: Session = Depends(get_db)):
    return recipes.read_one(db, recipes_id)

@app.put("/recipes/{recipes_id}", tags=["Recipes"])
def update_recipe(recipes_id: int, request: schemas.RecipeUpdate, db: Session = Depends(get_db)):
    return recipes.update(db, recipes_id, request)

@app.delete("/recipes/{recipes_id}", tags=["Recipes"])
def delete_recipe(recipes_id: int, db: Session = Depends(get_db)):
    recipes.delete(db, recipes_id)

#