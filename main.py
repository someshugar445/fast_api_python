import uvicorn
from fastapi import FastAPI, File, UploadFile
from fastapi.encoders import jsonable_encoder
import json
import os
from os.path import join, dirname, realpath
from typing import Optional
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None


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


if __name__ == "__main__":
    uvicorn.run(app, debug=True)
