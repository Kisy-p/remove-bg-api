from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from rembg import remove, new_session
import io

app = FastAPI()

# Charger le modèle une seule fois (léger)
try:
    print("[INFO] Chargement du modèle u2netp...")
    session = new_session("u2netp")
    print("[INFO] Modèle chargé avec succès")
except Exception as e:
    print(f"[ERREUR CRITIQUE] Échec du chargement du modèle : {e}")
    raise RuntimeError("Échec de l'initialisation du modèle")

@app.post("/remove-bg/")
async def remove_bg(file: UploadFile = File(...)):
    try:
        print("[INFO] Début du traitement")
        image_bytes = await file.read()

        if not image_bytes:
            raise HTTPException(status_code=400, detail="Fichier vide")

        print(f"[INFO] Taille du fichier : {len(image_bytes)} octets")

        # Suppression de l'arrière-plan
        output_bytes = remove(image_bytes, session=session)

        print("[INFO] Traitement terminé")
        return StreamingResponse(io.BytesIO(output_bytes), media_type="image/png")

    except Exception as e:
        print(f"[ERREUR] Exception pendant le traitement : {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")
