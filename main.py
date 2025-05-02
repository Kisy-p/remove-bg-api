from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
from rembg import remove, new_session
import io

app = FastAPI()

# On utilise le modèle le plus léger : u2netp (~5 Mo, RAM-friendly)
session = new_session("u2netp")

@app.post("/remove-bg/")
async def remove_bg(file: UploadFile = File(...)):
    image_bytes = await file.read()
    output = remove(image_bytes, session=session)
    return StreamingResponse(io.BytesIO(output), media_type="image/png")
