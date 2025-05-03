from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from rembg import remove, new_session
import io

app = FastAPI()

# Charger le modèle une seule fois au démarrage
try:
    session = new_session("u2netp")
    print("[INFO] Modèle 'u2netp' chargé avec succès")
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

        # Enregistrer temporairement l'image reçue (debug)
        file_path = f"/tmp/{file.filename}"
        with open(file_path, "wb") as buffer:
            buffer.write(image_bytes)

        print(f"[INFO] Image enregistrée temporairement : {file_path}")
        print(f"[INFO] Taille : {len(image_bytes)} octets")

        # Suppression de l’arrière-plan
        output_bytes = remove(image_bytes, session=session)

        print("[INFO] Traitement réussi")
        return StreamingResponse(io.BytesIO(output_bytes), media_type="image/png")

    except Exception as e:
        print(f"[ERREUR] {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")
