from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
from rembg import remove
import io

app = FastAPI()

@app.post("/remove-bg/")
async def remove_bg(file: UploadFile = File(...)):
    image_bytes = await file.read()
    result = remove(image_bytes)

    return StreamingResponse(io.BytesIO(result), media_type="image/png")
