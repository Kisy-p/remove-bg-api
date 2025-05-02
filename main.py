from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
import io

app = FastAPI()

@app.post("/remove-bg/")
async def remove_bg(file: UploadFile = File(...)):
    try:
        print("[INFO] Début du traitement")
        image_bytes = await file.read()

        if not image_bytes:
            raise HTTPException(status_code=400, detail="Fichier vide")

        print(f"[INFO] Taille du fichier reçu : {len(image_bytes)} octets")

        # ⚠️ Pour test uniquement : retourne le fichier tel quel
        return StreamingResponse(io.BytesIO(image_bytes), media_type="image/png")

    except Exception as e:
        print(f"[EXCEPTION] {str(e)}")
        raise HTTPException(status_code=500, detail="Erreur serveur")
