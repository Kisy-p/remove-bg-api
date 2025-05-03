from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
import io
import uvicorn
import logging
import sys
from rembg import remove
from PIL import Image
import traceback

# Config logs
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger("main")

app = FastAPI(title="API de suppression de fond d'image")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/remove-background/")
async def remove_background(file: UploadFile = File(...)):
    try:
        logger.info(f"Réception de l'image : {file.filename}")
        image_data = await file.read()

        if not image_data:
            logger.error("Aucune donnée d'image reçue")
            raise HTTPException(status_code=400, detail="Aucune donnée d'image reçue")

        try:
            input_image = Image.open(io.BytesIO(image_data)).convert("RGBA")
            logger.info(f"Image convertie: {input_image.mode}, {input_image.size}")
            input_image.save("/tmp/input_debug.png")
            logger.info("Image sauvegardée temporairement pour debug")
        except Exception as e:
            logger.error(f"Erreur d'ouverture: {e}")
            raise HTTPException(status_code=400, detail="Image invalide ou corrompue")

        try:
            logger.info("Suppression de l'arrière-plan...")
            output_image = remove(input_image)
            logger.info("Suppression réussie")
        except Exception as e:
            logger.error(f"Erreur rembg : {e}")
            logger.error(traceback.format_exc())
            raise HTTPException(status_code=500, detail="Erreur pendant la suppression du fond")

        img_bytes = io.BytesIO()
        output_image.save(img_bytes, format="PNG")
        img_bytes.seek(0)

        return Response(content=img_bytes.getvalue(), media_type="image/png")

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur inattendue : {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Erreur serveur inattendue")

@app.get("/")
def root():
    return {"message": "API de suppression de fond. Utilisez POST /remove-background/"}

@app.get("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    logger.info("Lancement serveur...")
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
