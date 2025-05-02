from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from rembg import remove
import io
import os

app = FastAPI()

# Préchargement du modèle
@app.on_event("startup")
async def load_model():
    test_input = io.BytesIO(b"fake_image_data").getvalue()
    await remove(test_input)

@app.post("/remove-background")
async def remove_background(file: UploadFile = File(...)):
    if not file.content_type.startswith('image/'):
        raise HTTPException(400, "Fichier non supporté")
    
    input_data = await file.read()
    output_data = await remove(input_data)
    
    return StreamingResponse(io.BytesIO(output_data), media_type="image/png")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
