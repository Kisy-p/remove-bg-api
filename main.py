from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from rembg import remove
import io
import os
import asyncio

app = FastAPI()

# === PRÉCHARGEMENT DU MODÈLE (évite les timeouts au premier appel) ===
@app.on_event("startup")
async def load_model():
    """Précharge le modèle ML au démarrage pour éviter les timeouts."""
    try:
        # Charge le modèle avec une image factice
        dummy_image = io.BytesIO(b"fake_image_data").getvalue()
        await remove(dummy_image)
    except Exception as e:
        raise RuntimeError(f"Échec du chargement du modèle : {e}")

# === ROUTE PRINCIPALE ===
@app.post("/remove-background")
async def remove_background(file: UploadFile = File(...)):
    """
    Reçoit une image, supprime son fond et renvoie l'image traitée.
    """
    # Vérifie que le fichier est une image
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Le fichier doit être une image.")

    # Lit le contenu du fichier
    input_data = await file.read()

    # Supprime le fond (asynchrone)
    output_data = await remove(input_data)

    # Renvoie l'image sans fond
    return StreamingResponse(io.BytesIO(output_data), media_type="image/png")

# === POINT D'ENTRÉE POUR RENDER ===
if __name__ == "__main__":
    import uvicorn
    # Utilise le port attribué par Render via la variable d'environnement
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 10000)))
