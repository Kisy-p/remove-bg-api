from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from rembg import remove, new_session
from PIL import Image
import io
import time

app = FastAPI()

# Chargement du modèle u2netp (léger)
try:
    session = new_session("u2netp")
    print("[INFO] Modèle u2netp chargé")
except Exception as e:
    print(f"[ERREUR CRITIQUE] Chargement du modèle : {e}")
    raise RuntimeError("Échec du chargement du modèle rembg")

@app.post("/remove-bg/")
async def remove_bg(file: UploadFile = File(...)):
    try:
        print("[INFO] Début du traitement")

        image_bytes = await file.read()
        if not image_bytes:
            raise HTTPException(status_code=400, detail="Fichier vide")

        print(f"[INFO] Taille : {len(image_bytes)} octets")

        # Vérification de l’image et sauvegarde temporaire
        try:
            image = Image.open(io.BytesIO(image_bytes))
            image.verify()
            image = Image.open(io.BytesIO(image_bytes))  # recharge après verify
            temp_path = f"/tmp/{int(time.time())}.png"
            image.save(temp_path)
            print(f"[INFO] Aperçu image sauvegardé dans {temp_path}")
        except Exception as img_err:
            print(f"[ERREUR] Image invalide : {img_err}")
            raise HTTPException(status_code=400, detail="Image invalide")

        # Appel à rembg
        try:
            output_bytes = remove(image_bytes, session=session)
            print("[INFO] remove() exécuté avec succès")
        except Exception as rembg_err:
            print(f"[ERREUR REMBG] {rembg_err}")
            raise HTTPException(status_code=500, detail="Erreur rembg")

        # Retourner l’image transformée
        return StreamingResponse(io.BytesIO(output_bytes), media_type="image/png")

    except HTTPException:
        raise
    except Exception as e:
        print(f"[ERREUR] Exception générale : {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")
