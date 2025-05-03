from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from rembg import remove, new_session
import io
import os
import time

app = FastAPI()

# Chargement du modèle léger
try:
    session = new_session("u2netp")
    print("[INFO] Modèle u2netp chargé avec succès.")
except Exception as e:
    print(f"[ERREUR CRITIQUE] Échec du chargement du modèle : {e}")
    raise RuntimeError("Impossible de charger le modèle u2netp")

@app.post("/remove-bg/")
async def remove_bg(file: UploadFile = File(...)):
    try:
        print("[INFO] Début du traitement")

        image_bytes = await file.read()

        if not image_bytes:
            raise HTTPException(status_code=400, detail="Fichier vide")

        print(f"[INFO] Taille de l'image reçue : {len(image_bytes)} octets")

        # Debug : Sauvegarde temporaire
        timestamp = str(int(time.time()))
        temp_path = f"/tmp/{timestamp}_{file.filename}"
        with open(temp_path, "wb") as temp_file:
            temp_file.write(image_bytes)
        print(f"[INFO] Image sauvegardée temporairement : {temp_path}")

        # Traitement de l'image
        result = remove(image_bytes, session=session)
        print("[INFO] Arrière-plan supprimé avec succès")

        return StreamingResponse(io.BytesIO(result), media_type="image/png")

    except Exception as e:
        print(f"[ERREUR] {str(e)}")
        raise HTTPException(status_code=500, detail="Erreur serveur")
