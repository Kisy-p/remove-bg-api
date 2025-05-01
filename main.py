from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
from rembg import remove
from PIL import Image
import io

app = FastAPI()

@app.post("/remove-bg/")
async def remove_bg(file: UploadFile = File(...)):
    # Lire les données brutes de l'image
    image_bytes = await file.read()
    input_image = Image.open(io.BytesIO(image_bytes))

    # Supprimer l’arrière-plan
    output_bytes = remove(image_bytes)

    # Retourner l’image traitée directement
    return StreamingResponse(io.BytesIO(output_bytes), media_type="image/png")
