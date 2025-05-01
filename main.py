from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from rembg import remove
from PIL import Image
import io
import uuid
import os

app = FastAPI()

@app.post("/remove-bg/")
async def remove_background(file: UploadFile = File(...)):
    contents = await file.read()
    input_image = Image.open(io.BytesIO(contents))
    output_image = remove(input_image)

    output_filename = f"{uuid.uuid4()}.png"
    output_path = f"/tmp/{output_filename}"
    output_image.save(output_path)

    return FileResponse(output_path, media_type="image/png", filename="sans_fond.png")
