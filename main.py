from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from rembg import remove, new_session
import io

app = FastAPI()

# Charger le modèle léger une seule fois
session = new_session("u2netp")

@app.post("/remove-bg/")
async def remove_bg(file: UploadFile = File(...)):
    try:
        print("[INFO] Début du traitement")
        image_bytes = await file.read()
        print(f"[INFO] Taille : {len(image_bytes)}")

        # Appliquer la suppression de fond
        output_bytes = remove(image_bytes, session=session)
        print("[INFO] Traitement réussi")

        return StreamingResponse(io.BytesIO(output_bytes), media_type="image/png")

    except Exception as e:
        print(f"[ERREUR] {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")
