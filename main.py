from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

# In-memory "database"
fake_db = {}


# Data model for an item
class Item(BaseModel):
    id: int
    name: str
    description: str
    price: float
    on_offer: bool

# Create (POST)
@app.post("/items/", status_code=201)
def create_item(item:Item):
    if item.id in fake_db:
        raise HTTPException(status_code=400, detail="Item ID already exists")
    fake_db[item.id]= item
    return{"message":"Item created successfully","item":item}

# Read All (GET)
@app.get("/items/", response_model=List[Item])
def get_items():
    return list(fake_db.values())

# Read Single (GET)
@app.get("/items/{item_id}")
def get_item(item_id:int):
    if item_id not in fake_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return fake_db[item_id]

# Update (PUT)
@app.put("/items/{item_id}")
def update_item(item_id:int, updated_item:Item):
    if item_id not in fake_db:
        raise HTTPException(status_code=404, detail="Item not found")
    fake_db[item_id] = updated_item
    return{"message":"Item updated successfully","item":updated_item}

# Delete (DELETE)
@app.delete("/items/{item_id}")
def delete_item(item_id:int):
    if item_id not in fake_db:
        raise HTTPException(status_code=404, detail="Item not found")
    del fake_db[item_id]
    return{"message":"Item deleted successfully"}
