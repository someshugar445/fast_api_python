import uvicorn
from fastapi import FastAPI, File, UploadFile
from fastapi.encoders import jsonable_encoder
import json
import os
from os.path import join, dirname, realpath
from typing import Optional
from pydantic import BaseModel
from fastapi.responses import HTMLResponse

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None


@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <html>
        <h1>
            <title>Fast api demo</title>
        </h1>
        <body>
            <h1>Welcome to Python Fast api demo</h1>
            <p>Click on below link to execute rest apis</p>
            <p>
             <a href="http://127.0.0.1:8000/docs">Click here</a>
            </p>
        </body>
    </html>
    """


@app.get("/items/{name}")
def query_record(name):
    try:
        with open('data.txt', 'r') as f:
            data = f.read()
            all_records = json.loads(data)
        if name != 'all':
            record_found = False
            for record in all_records:
                if record['name'] == name:
                    name_record = record
                    record_found = True
            if record_found:
                return name_record
            else:
                return "Error: name not found"
        else:
            return all_records
    except Exception as e:
        print("Exception", e)


@app.post("/items/")
async def create_item(item: Item):
    new_record = item.dict()
    with open('data.txt', 'r') as f:
        data = f.read()
        old_records = json.loads(data)
    print(old_records)
    record_not_found = False
    for record in old_records:
        if record['name'] != new_record['name']:
            print(record['name'])
            print(new_record['name'])
            record_not_found = True
    if not old_records:
        old_records.append(new_record)
        with open('data.txt', 'w') as f:
            f.write(json.dumps(old_records, indent=2))
    elif record_not_found:
        old_records.append(new_record)
        with open('data.txt', 'w') as f:
            f.write(json.dumps(old_records, indent=2))
    else:
        print("INFO': 'Product already exists")
    return new_record


@app.put("/items/")
async def update_record(item: Item):
    new_record = item.dict()
    with open('data.txt', 'r') as f:
        data = f.read()
        records = json.loads(data)
    record_found = False
    for r in records:
        if r['name'] == new_record['name']:
            old_record = r
            record_found = True
    if record_found:
        records.remove(old_record)
        records.append(new_record)
    else:
        records.append(new_record)
    with open('data.txt', 'w') as f:
        f.write(json.dumps(records, indent=2))
    return records


@app.delete("/items/")
def delete_record(name):
    with open('data.txt', 'r') as f:
        data = f.read()
        records = json.loads(data)
    record_found = False
    if name != "all":
        for record in records:
            if record['name'] == name:
                record_found = True
                name_record = record
        if record_found:
            records.remove(name_record)
            with open('data.txt', 'w') as f:
                f.write(json.dumps(records, indent=2))
            return {'response': 'record has been deleted'}
        else:
            return {'INFO': 'name not found'}
    else:
        for record in records:
            records.remove(record)
        with open('data.txt', 'w') as f:
            f.write(json.dumps(records, indent=2))
        return {'response': 'All records has been deleted'}


if __name__ == "__main__":
    uvicorn.run(app, debug=True)
