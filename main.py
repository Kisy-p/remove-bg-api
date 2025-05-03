from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
import shutil
import io
import os

app = FastAPI()

@app.post("/remove-bg/")
async def remove_bg(file: UploadFile = File(...)):
    try:
        print("[INFO] Début du traitement")

        image_bytes = await file.read()

        if not image_bytes:
            raise HTTPException(status_code=400, detail="Fichier vide")

        file_path = f"/tmp/{file.filename}"
        
        # Sauvegarder l'image brute pour test
        with open(file_path, "wb") as buffer:
            buffer.write(image_bytes)

        print(f"[INFO] Image enregistrée temporairement : {file_path}")
        print(f"[INFO] Taille : {len(image_bytes)} octets")

        # ⚠️ Test : retourne l’image telle quelle
        return StreamingResponse(io.BytesIO(image_bytes), media_type="image/png")

    except Exception as e:
        print(f"[ERREUR] {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")
