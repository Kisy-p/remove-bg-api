from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from rembg import remove
import io
import os

# Définir le modèle léger
os.environ["U2NET_HOME"] = "/opt/render/.u2net"  # optionnel
os.environ["REMBG_SESSION"] = "u2netp"

app = FastAPI()

@app.post("/remove-bg/")
async def remove_bg(file: UploadFile = File(...)):
    try:
        print("[INFO] Début du traitement")
        image_bytes = await file.read()
        print(f"[INFO] Taille : {len(image_bytes)}")

        output_bytes = remove(image_bytes, session="u2netp")
        return StreamingResponse(io.BytesIO(output_bytes), media_type="image/png")

    except Exception as e:
        print(f"[ERREUR] {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")
