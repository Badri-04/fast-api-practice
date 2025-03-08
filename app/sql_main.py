from typing import Optional
from fastapi import Body, FastAPI, Response, status, HTTPException
from pydantic import BaseModel
import psycopg
from psycopg.rows import dict_row

app = FastAPI()

try:
    conn = psycopg.connect(
        host="localhost",
        dbname="fastapi_db",
        user="postgres",
        password="p0stgres1"
    )
    cursor = conn.cursor(
        row_factory=dict_row
    )
    print("Database connected successfully")
except Exception as e:
    print(e)

class Item(BaseModel):
    name: str
    count: int = 0
    rating: Optional[int] = None


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/items/")
def getItems():
    cursor.execute("SELECT * FROM items")
    items = cursor.fetchall()
    return {"data": items}


@app.get("/item/{item_id}")
def getItem(item_id: int): # , response: Response):

    cursor.execute("SELECT * FROM items WHERE id = %s", (item_id,))
    item = cursor.fetchone()
    if not item:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": "Item not found"}
        raise HTTPException(status_code=404, detail="Item not found") # best practice
    
    return {"data": item}


@app.post("/addItem/", status_code=status.HTTP_201_CREATED)
def addItem(payload: Item):
    cursor.execute("INSERT INTO items (name, count, rating) VALUES (%s, %s, %s) RETURNING *", (payload.name, payload.count, payload.rating))
    item = cursor.fetchone()
    conn.commit()
    return {"data": item}


@app.delete("/deleteItem/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def deleteItem(item_id: int):
    cursor.execute("DELETE FROM items WHERE id = %s RETURNING *", (item_id,))
    item = cursor.fetchone()
    conn.commit()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    # perform delete
    return Response(status_code=status.HTTP_204_NO_CONTENT) # when 204 is statuscode we shouldn't send any other data


@app.put("/updateItem/{item_id}")
def updateItem(item_id: int, payload: Item):
    cursor.execute("UPDATE items SET name = %s WHERE id = %s RETURNING *", (payload.name, item_id))
    item = cursor.fetchone()
    conn.commit()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    # perform update
    return {"data": item}