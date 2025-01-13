from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import pymysql
from typing import List, Optional
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import os

app = FastAPI()
load_dotenv()
database = os.getenv('DATABASE')
password = os.getenv('PASSWORD')


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None


def get_db():
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password=password,
        database=database,
        cursorclass=pymysql.cursors.DictCursor
    )
    try:
        yield connection
    finally:
        connection.close()


@app.get('/')
def read_root():
    return {"message": "Welcome to the FastAPI app with MySQL using PyMySQL!"}


@app.post("/items/", response_model=Item)
async def create_item(item: Item, db=Depends(get_db)):
    try:
        with db.cursor() as cursor:
            sql = "INSERT INTO products (name, description, price, tax) VALUES (%s, %s, %s, %s)"
            cursor.execute(
                sql, (item.name, item.description, item.price, item.tax))
            db.commit()
        return JSONResponse({"message": "Data saved successfully"})
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.get("/items/", response_model=List[Item])
async def get_items(db=Depends(get_db)):
    try:
        with db.cursor() as cursor:
            cursor.execute(
                "SELECT id, name, description, price, tax FROM products")
            result = cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.get("/items/{item_id}", response_model=Item)
async def get_item(item_id: int, db=Depends(get_db)):
    try:
        with db.cursor() as cursor:
            cursor.execute(
                "SELECT id, name, description, price, tax FROM products WHERE id = %s", (item_id,))
            item = cursor.fetchone()
        if item is None:
            raise HTTPException(status_code=404, detail="Item not found")
        return item
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: int, item: Item, db=Depends(get_db)):
    try:
        with db.cursor() as cursor:
            cursor.execute(
                "UPDATE products SET name = %s, description = %s, price = %s, tax = %s WHERE id = %s",
                (item.name, item.description, item.price, item.tax, item_id)
            )
            db.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Item not found")
        return item
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.delete("/items/{item_id}")
async def delete_item(item_id: int, db=Depends(get_db)):
    try:
        with db.cursor() as cursor:
            cursor.execute("DELETE FROM products WHERE id = %s", (item_id,))
            db.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Item not found")
        return {"message": "Item deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
