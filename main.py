from fastapi import FastAPI, File, UploadFile, HTTPException
from rembg import remove
from fastapi.responses import StreamingResponse
import io

app = FastAPI()

@app.post("/remove-background")
async def remove_background(file: UploadFile = File(...)):
    # Vérification du type de fichier
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="Le fichier doit être une image")
    
    # Lecture du fichier
    input_image = await file.read()
    
    # Suppression du fond
    output_image = remove(input_image)
    
    # Création d'un flux mémoire
    result = io.BytesIO(output_image)
    
    # Retour de l'image traitée
    return StreamingResponse(result, media_type="image/png")

# Point d'entrée pour Render
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)
