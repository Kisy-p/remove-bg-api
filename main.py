from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from rembg import remove, new_session
import io

app = FastAPI()

@app.post("/remove-bg/")
async def remove_bg(file: UploadFile = File(...)):
    try:
        image_bytes = await file.read()

        if not image_bytes:
            raise HTTPException(status_code=400, detail="Fichier vide")

        session = new_session("u2netp")  # modèle léger
        output = remove(image_bytes, session=session)

        return StreamingResponse(io.BytesIO(output), media_type="image/png")

    except Exception as e:
        print(f"[ERREUR SERVEUR] {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")
