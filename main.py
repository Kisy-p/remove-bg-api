from fastapi import FastAPI, File, UploadFile
from fastapi.responses import Response
import io
import uvicorn
from rembg import remove
from PIL import Image

app = FastAPI(title="API de suppression de fond d'image")

@app.post("/remove-background/")
async def remove_background(file: UploadFile = File(...)):
    # Lire l'image téléchargée
    image_data = await file.read()
    input_image = Image.open(io.BytesIO(image_data))
    
    # Supprimer le fond de l'image
    output_image = remove(input_image)
    
    # Convertir l'image en bytes pour la réponse
    img_byte_arr = io.BytesIO()
    output_image.save(img_byte_arr, format=input_image.format if input_image.format else "PNG")
    img_byte_arr.seek(0)
    
    # Renvoyer l'image traitée
    return Response(
        content=img_byte_arr.getvalue(), 
        media_type=f"image/{input_image.format.lower() if input_image.format else 'png'}"
    )

@app.get("/")
def read_root():
    return {"message": "API de suppression de fond d'image. Utilisez /remove-background/ pour traiter une image."}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
