from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
from rembg import remove
from PIL import Image
import io

app = FastAPI()

@app.post("/remove-bg/")
async def remove_bg(file: UploadFile = File(...)):
    # Lire le fichier envoyé
    image_bytes = await file.read()

    # Charger l'image avec PIL
    input_image = Image.open(io.BytesIO(image_bytes))

    # Supprimer l'arrière-plan
    output_image = remove(input_image)  # <-- on passe une image PIL, pas des bytes

    # Convertir l'image résultante en flux binaire
    buffered = io.BytesIO()
    output_image.save(buffered, format="PNG")
    buffered.seek(0)

    return StreamingResponse(buffered, media_type="image/png")
