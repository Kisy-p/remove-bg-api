from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from rembg import remove, new_session
import io
import os
import time

app = FastAPI()

try:
    print("[INFO] Initialisation du modèle u2netp...")
    session = new_session("u2netp")
except Exception as e:
    print(f"[ERREUR CRITIQUE] Échec du chargement du modèle : {e}")
    raise RuntimeError("Impossible de charger le modèle rembg")

@app.post("/remove-bg/")
async def remove_bg(file: UploadFile = File(...)):
    try:
        print("[INFO] Début du traitement")
        image_bytes = await file.read()

        if not image_bytes:
            raise HTTPException(status_code=400, detail="Fichier vide")

        # Enregistrement temporaire pour debug
        filename = f"/tmp/{int(time.time())}.png"
        with open(filename, "wb") as f:
            f.write(image_bytes)
        print(f"[INFO] Image enregistrée temporairement : {filename}")
        print(f"[INFO] Taille du fichier : {len(image_bytes)} octets")

        # Suppression du fond
        output = remove(image_bytes, session=session)

        return StreamingResponse(io.BytesIO(output), media_type="image/png")

    except Exception as e:
        print(f"[ERREUR SERVEUR] {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")
