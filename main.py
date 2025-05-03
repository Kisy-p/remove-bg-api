from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
import io
import logging
import sys
from rembg import remove, new_session
from PIL import Image

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

# Initialisation FastAPI
app = FastAPI(title="API de suppression d'arrière-plan d'image")

# Middleware CORS (accès cross-origin autorisé)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Chargement du modèle léger u2netp
try:
    session = new_session("u2netp")
    logger.info("Modèle u2netp chargé avec succès")
except Exception as e:
    logger.critical(f"Erreur critique lors du chargement du modèle : {e}")
    raise

@app.post("/remove-background/", summary="Supprimer le fond d'une image", description="Supprime l'arrière-plan d'une image envoyée au format JPG, PNG, etc.")
async def remove_background(file: UploadFile = File(...)):
    try:
        logger.info(f"Réception de l'image : {file.filename}")
        image_data = await file.read()

        if not image_data:
            logger.error("Aucune donnée d'image reçue")
            raise HTTPException(status_code=400, detail="Fichier vide")

        # Vérification de l'image
        try:
            input_image = Image.open(io.BytesIO(image_data)).convert("RGBA")
            logger.info(f"Image ouverte : {input_image.format}, {input_image.size}")
        except Exception as e:
            logger.error(f"Erreur d'ouverture de l'image : {e}")
            raise HTTPException(status_code=400, detail="Image invalide")

        # Suppression de l'arrière-plan
        try:
            logger.info("Suppression de l'arrière-plan...")
            result = remove(input_image, session=session)
        except Exception as e:
            logger.error(f"Erreur lors du traitement : {e}")
            raise HTTPException(status_code=500, detail="Erreur pendant le traitement de l'image")

        # Conversion en bytes pour la réponse
        output_buffer = io.BytesIO()
        result.save(output_buffer, format="PNG")
        output_buffer.seek(0)

        logger.info("Image traitée avec succès")
        return Response(content=output_buffer.getvalue(), media_type="image/png")

    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Erreur inattendue : {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")

@app.get("/", summary="Page d'accueil", description="Affiche un message d'accueil.")
def read_root():
    logger.info("Accès à la racine")
    return {"message": "Bienvenue sur l'API de suppression de fond d'image. POST /remove-background pour traiter."}

@app.get("/health", summary="Vérification de l'état", description="Renvoie le statut de l'API.")
def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    logger.info("Démarrage de l'application")
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
