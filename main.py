from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from rembg import remove, new_session
import io
import traceback

app = FastAPI()

@app.post("/remove-bg/")
async def remove_bg(file: UploadFile = File(...)):
    try:
        print("[INFO] Début du traitement")
        image_bytes = await file.read()

        if not image_bytes:
            raise HTTPException(status_code=400, detail="Fichier vide")

        print(f"[INFO] Taille du fichier reçu : {len(image_bytes)} octets")

        # Charge explicitement une session avec le modèle U2NET (le plus précis)
        session = new_session("u2net")
        output_bytes = remove(image_bytes, session=session)

        print(f"[INFO] Taille de l'image retournée : {len(output_bytes)} octets")

        return StreamingResponse(io.BytesIO(output_bytes), media_type="image/png")

    except Exception as e:
        print(f"[EXCEPTION] {str(e)}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Erreur serveur")
