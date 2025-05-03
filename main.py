from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from rembg import remove, new_session
from PIL import Image
import io
import os
import time

app = FastAPI()

# Crée un dossier temporaire s'il n'existe pas
os.makedirs("/tmp/images", exist_ok=True)

# Précharger le modèle une fois au lancement
try:
    print("[INFO] Chargement du modèle u2netp...")
    session = new_session("u2netp")
    print("[INFO] Modèle chargé avec succès.")
except Exception as e:
    print(f"[ERREUR CRITIQUE] Échec du chargement du modèle : {e}")
    raise

@app.post("/remove-bg/")
async def remove_bg(file: UploadFile = File(...)):
    try:
        print("[INFO] Début du traitement")
        image_bytes = await file.read()

        if not image_bytes:
            raise HTTPException(status_code=400, detail="Fichier vide")

        print(f"[INFO] Taille du fichier reçu : {len(image_bytes)} octets")

        # Sauvegarder temporairement l'image reçue
        filename = f"/tmp/images/{int(time.time())}.png"
        with open(filename, "wb") as f:
            f.write(image_bytes)
        print(f"[INFO] Image enregistrée temporairement : {filename}")

        # Traitement avec rembg
        output_bytes = remove(image_bytes, session=session)

        print("[INFO] Suppression de fond réussie.")
        return StreamingResponse(io.BytesIO(output_bytes), media_type="image/png")

    except Exception as e:
        print(f"[ERREUR] {str(e)}")
        raise HTTPException(status_code=500, detail="Erreur serveur")
