from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import Response, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import io
import uvicorn
import logging
import sys
import os
import time
from rembg import remove
from PIL import Image

# Configuration des logs
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

app = FastAPI(title="API de suppression de fond d'image")

# Ajouter CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permet toutes les origines
    allow_credentials=True,
    allow_methods=["*"],  # Permet toutes les méthodes
    allow_headers=["*"],  # Permet tous les headers
)

# Précharger le modèle au démarrage
@app.on_event("startup")
async def startup_event():
    logger.info("Initialisation du serveur...")
    try:
        # Tester rembg avec une petite image
        logger.info("Test de rembg avec une petite image...")
        test_img = Image.new('RGB', (100, 100), color = (73, 109, 137))
        start_time = time.time()
        remove(test_img)
        logger.info(f"Test de rembg réussi en {time.time() - start_time:.2f} secondes")
    except Exception as e:
        logger.error(f"Erreur lors du test de rembg: {str(e)}")
        # Continuer malgré l'erreur

@app.post("/remove-background/")
async def remove_background(file: UploadFile = File(...)):
    try:
        logger.info(f"Réception d'une image: {file.filename}")
        
        # Lire l'image téléchargée
        image_data = await file.read()
        
        if not image_data:
            logger.error("Aucune donnée d'image reçue")
            raise HTTPException(status_code=400, detail="Aucune donnée d'image reçue")
        
        # Ouvrir l'image
        try:
            input_image = Image.open(io.BytesIO(image_data))
            logger.info(f"Image ouverte: {input_image.format}, {input_image.size}")
        except Exception as e:
            logger.error(f"Erreur lors de l'ouverture de l'image: {str(e)}")
            raise HTTPException(status_code=400, detail="Format d'image non valide")
        
        # Supprimer le fond de l'image
        try:
            logger.info("Traitement de l'image en cours...")
            start_time = time.time()
            output_image = remove(input_image)
            logger.info(f"Fond supprimé avec succès en {time.time() - start_time:.2f} secondes")
        except Exception as e:
            logger.error(f"Erreur lors de la suppression du fond: {str(e)}")
            raise HTTPException(status_code=500, detail="Erreur lors du traitement de l'image")
        
        # Convertir l'image en bytes pour la réponse
        img_byte_arr = io.BytesIO()
        output_format = input_image.format if input_image.format else "PNG"
        output_image.save(img_byte_arr, format=output_format)
        img_byte_arr.seek(0)
        
        logger.info(f"Image traitée et convertie en {output_format}")
        
        # Renvoyer l'image traitée
        return Response(
            content=img_byte_arr.getvalue(), 
            media_type=f"image/{output_format.lower()}"
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Erreur inattendue: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erreur inattendue: {str(e)}")

@app.get("/")
def read_root():
    logger.info("Accès à la racine")
    return {"message": "API de suppression de fond d'image. Utilisez /remove-background/ pour traiter une image."}

@app.get("/health")
def health_check():
    # Vérifier l'environnement
    env_info = {
        "python_version": sys.version,
        "memory_info": os.popen('free -h').read() if sys.platform.startswith('linux') else "Non disponible"
    }
    return {"status": "ok", "env_info": env_info}

@app.get("/debug")
def debug_info():
    # Fournir des informations de débogage
    import psutil
    
    mem = psutil.virtual_memory()
    
    debug_data = {
        "memory": {
            "total": f"{mem.total / (1024**3):.2f} GB",
            "available": f"{mem.available / (1024**3):.2f} GB",
            "used": f"{mem.used / (1024**3):.2f} GB",
            "percent": f"{mem.percent}%"
        },
        "cpu": {
            "usage": f"{psutil.cpu_percent(interval=1)}%",
            "cores": psutil.cpu_count(logical=True)
        },
        "disk": {
            "total": f"{psutil.disk_usage('/').total / (1024**3):.2f} GB",
            "used": f"{psutil.disk_usage('/').used / (1024**3):.2f} GB",
            "free": f"{psutil.disk_usage('/').free / (1024**3):.2f} GB",
            "percent": f"{psutil.disk_usage('/').percent}%"
        },
        "python_version": sys.version,
        "platform": sys.platform
    }
    
    return debug_data

if __name__ == "__main__":
    logger.info("Démarrage du serveur...")
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))


@app.post("/remove-background/")
async def remove_background(file: UploadFile = File(...)):
    try:
        logger.info(f"Réception d'une image: {file.filename}")
        
        # Lire l'image téléchargée
        image_data = await file.read()
        
        if not image_data:
            logger.error("Aucune donnée d'image reçue")
            raise HTTPException(status_code=400, detail="Aucune donnée d'image reçue")
        
        # Ouvrir l'image
        try:
            input_image = Image.open(io.BytesIO(image_data))
            logger.info(f"Image ouverte: {input_image.format}, {input_image.size}")
        except Exception as e:
            logger.error(f"Erreur lors de l'ouverture de l'image: {str(e)}")
            raise HTTPException(status_code=400, detail="Format d'image non valide")
        
        # Supprimer le fond de l'image
        try:
            logger.info("Traitement de l'image en cours...")
            start_time = time.time()
            output_image = remove(input_image)
            logger.info(f"Fond supprimé avec succès en {time.time() - start_time:.2f} secondes")
        except Exception as e:
            logger.error(f"Erreur lors de la suppression du fond: {str(e)}")
            raise HTTPException(status_code=500, detail="Erreur lors du traitement de l'image")
        
        # Convertir l'image en bytes pour la réponse
        img_byte_arr = io.BytesIO()
        output_format = input_image.format if input_image.format else "PNG"
        output_image.save(img_byte_arr, format=output_format)
        img_byte_arr.seek(0)
        
        logger.info(f"Image traitée et convertie en {output_format}")
        
        # Renvoyer l'image traitée
        return Response(
            content=img_byte_arr.getvalue(), 
            media_type=f"image/{output_format.lower()}"
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Erreur inattendue: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erreur inattendue: {str(e)}")

@app.get("/")
def read_root():
    logger.info("Accès à la racine")
    return {"message": "API de suppression de fond d'image. Utilisez /remove-background/ pour traiter une image."}

@app.get("/health")
def health_check():
    # Vérifier l'environnement
    env_info = {
        "python_version": sys.version,
        "memory_info": os.popen('free -h').read() if sys.platform.startswith('linux') else "Non disponible"
    }
    return {"status": "ok", "env_info": env_info}

@app.get("/debug")
def debug_info():
    # Fournir des informations de débogage
    import psutil
    
    mem = psutil.virtual_memory()
    
    debug_data = {
        "memory": {
            "total": f"{mem.total / (1024**3):.2f} GB",
            "available": f"{mem.available / (1024**3):.2f} GB",
            "used": f"{mem.used / (1024**3):.2f} GB",
            "percent": f"{mem.percent}%"
        },
        "cpu": {
            "usage": f"{psutil.cpu_percent(interval=1)}%",
            "cores": psutil.cpu_count(logical=True)
        },
        "disk": {
            "total": f"{psutil.disk_usage('/').total / (1024**3):.2f} GB",
            "used": f"{psutil.disk_usage('/').used / (1024**3):.2f} GB",
            "free": f"{psutil.disk_usage('/').free / (1024**3):.2f} GB",
            "percent": f"{psutil.disk_usage('/').percent}%"
        },
        "python_version": sys.version,
        "platform": sys.platform
    }
    
    return debug_data

if __name__ == "__main__":
    logger.info("Démarrage du serveur...")
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))

