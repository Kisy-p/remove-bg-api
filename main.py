from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
from rembg import remove, new_session
from PIL import Image
import io

app = FastAPI()

# Charger une seule fois le modèle
session = new_session("u2net")

@app.post("/remove-bg/")
async def remove_bg(file: UploadFile = File(...)):
    image_bytes = await file.read()
    input_image = Image.open(io.BytesIO(image_bytes))
    output_image = remove(input_image, session=session)

    buffered = io.BytesIO()
    output_image.save(buffered, format="PNG")
    buffered.seek(0)

    return StreamingResponse(buffered, media_type="image/png")
