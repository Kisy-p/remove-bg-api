from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from rembg import remove, new_session
import io

app = FastAPI()

try:
    session = new_session("u2netp")  # modèle léger
except Exception as e:
    print(f"[ERREUR CRITIQUE] Chargement modèle : {e}")
    raise

@app.post("/remove-bg/")
async def remove_bg(file: UploadFile = File(...)):
    try:
        print("[INFO] Début du traitement")
        image_bytes = await file.read()

        if not image_bytes:
            raise HTTPException(status_code=400, detail="Fichier vide")

        print(f"[INFO] Taille : {len(image_bytes)}")

        output_bytes = remove(image_bytes, session=session)

        print("[INFO] Traitement réussi")
        return StreamingResponse(io.BytesIO(output_bytes), media_type="image/png")

    except Exception as e:
        print(f"[ERREUR] {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")
