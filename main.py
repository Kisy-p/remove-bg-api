from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
from rembg import remove, new_session
from PIL import Image
import io
import logging

app = FastAPI()

# Logger pour Render
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("uvicorn")

session = new_session("u2net")

@app.post("/remove-bg/")
async def remove_bg(file: UploadFile = File(...)):
    try:
        logger.info("Lecture du fichier...")
        image_bytes = await file.read()

        logger.info("Ouverture avec PIL...")
        input_image = Image.open(io.BytesIO(image_bytes))

        logger.info("Suppression du fond...")
        output_image = remove(input_image, session=session)

        logger.info("Conversion PNG...")
        buffered = io.BytesIO()
        output_image.save(buffered, format="PNG")
        buffered.seek(0)

        logger.info("Envoi de la réponse PNG.")
        return StreamingResponse(buffered, media_type="image/png")

    except Exception as e:
        logger.error(f"Erreur : {e}")
        raise e
