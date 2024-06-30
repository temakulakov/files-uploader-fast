from fastapi import FastAPI, File, UploadFile, Form, Query
from fastapi.responses import JSONResponse
import os
from typing import List, Optional
import hashlib
import datetime

app = FastAPI()

# Путь для хранения загруженных файлов
UPLOAD_FOLDER = 'uploaded_files'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Хранилище данных
data_store = []

def generate_file_name(file_name: str) -> str:
    hash_object = hashlib.sha256((file_name + str(datetime.datetime.now())).encode())
    hex_dig = hash_object.hexdigest()
    file_extension = file_name.split('.')[-1]
    new_file_name = f"{file_name.split('.')[0]}_{hex_dig}.{file_extension}"
    return new_file_name

@app.post("/api/add")
async def add_entry(id: int = Form(...), value: str = Form(...), file: UploadFile = File(...)):
    original_file_name = file.filename
    new_file_name = generate_file_name(original_file_name)
    file_path = os.path.join(UPLOAD_FOLDER, new_file_name)
    with open(file_path, 'wb') as f:
        f.write(await file.read())

    entry = {"id": id, "value": value, "files": file_path}
    data_store.append(entry)
    return JSONResponse(content={"message": "Entry added successfully", "data" : {
        "id": id,
        "value": value,
        "file": file_path
		}}, status_code=200)

@app.get("/api/get")
async def get_entry(id: Optional[int] = Query(None), value: Optional[str] = Query(None)):
    results = [entry for entry in data_store if (id is None or entry["id"] == id) and (value is None or entry["value"] == value)]
    return JSONResponse(content=results, status_code=200)

@app.delete("/api/delete")
async def delete_entry(id: int = Query(...), value: str = Query(...)):
    global data_store
    new_data_store = []
    for entry in data_store:
        if entry["id"] == id and entry["value"] == value:
            os.remove(entry["files"])
        else:
            new_data_store.append(entry)
    data_store = new_data_store
    return JSONResponse(content={"message": "Entry deleted successfully"}, status_code=200)

@app.get("/api/getAll")
async def get_all_entries(id: int = Query(...)):
    results = [entry for entry in data_store if entry["id"] == id]
    return JSONResponse(content=results, status_code=200)
