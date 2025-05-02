from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
import io
import subprocess
import tempfile
import os

app = FastAPI()

@app.get("/")
async def ping():
    return {"status": "ok"}

@app.post("/remove-bg/")
async def remove_bg(file: UploadFile = File(...)):
    try:
        image_bytes = await file.read()

        if not image_bytes:
            raise HTTPException(status_code=400, detail="Fichier vide")

        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as input_tmp:
            input_tmp.write(image_bytes)
            input_path = input_tmp.name

        output_path = input_path.replace(".png", "_out.png")

        print(f"[DEBUG] Input path: {input_path}")
        print(f"[DEBUG] Output path: {output_path}")

        result = subprocess.run(
            ["rembg", "-v", "i", input_path, output_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        print(f"[rembg STDOUT] {result.stdout}")
        print(f"[rembg STDERR] {result.stderr}")

        if result.returncode != 0:
            raise HTTPException(status_code=500, detail="Échec du traitement de l'image")

        if not os.path.exists(output_path):
            raise HTTPException(status_code=500, detail="Fichier de sortie non trouvé")

        with open(output_path, "rb") as out_file:
            processed_image = out_file.read()

        os.remove(input_path)
        os.remove(output_path)

        return StreamingResponse(io.BytesIO(processed_image), media_type="image/png")

    except Exception as e:
        print(f"[EXCEPTION] {str(e)}")
        raise HTTPException(status_code=500, detail="Erreur serveur")
