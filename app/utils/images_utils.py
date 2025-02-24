import os
import shutil
import uuid
from fastapi import UploadFile

UPLOAD_DIR = "uploads/"
os.makedirs(UPLOAD_DIR, exist_ok=True)  

def save_image(file: UploadFile) -> str:
    ext = file.filename.split(".")[-1]
    unique_name = f"{uuid.uuid4()}.{ext}" 
    file_path = os.path.join(UPLOAD_DIR, unique_name)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return file_path

def delete_image(file_path: str):
    try:
        os.remove(file_path)
    except FileNotFoundError:
        pass  
