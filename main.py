from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
from rembg import remove
from PIL import Image
import io

app = FastAPI()

@app.post("/remove-bg/")
async def remove_bg(file: UploadFile = File(...)):
    image_bytes = await file.read()
    output_bytes = remove(image_bytes)

    output_stream = io.BytesIO(output_bytes)
    output_stream.seek(0)  # Important !

    return StreamingResponse(output_stream, media_type="image/png")
