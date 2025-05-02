from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
import io

app = FastAPI()

@app.get("/")
async def ping():
    return {"status": "ok"}

@app.post("/remove-bg/")
async def remove_bg(file: UploadFile = File(...)):
    try:
        image_bytes = await file.read()

        if not image_bytes:
            raise HTTPException(status_code=400, detail="Fichier vide")

        print(f"==> Fichier reçu : {len(image_bytes)} octets, type: {file.content_type}")

        return StreamingResponse(io.BytesIO(image_bytes), media_type="image/png")

    except Exception as e:
        print(f"ERREUR: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")
