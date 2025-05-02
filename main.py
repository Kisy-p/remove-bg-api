from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from rembg import remove, new_session
import io

app = FastAPI()

session = new_session("u2netp")

@app.post("/remove-bg/")
async def remove_bg(file: UploadFile = File(...)):
    try:
        if file.content_type not in ["image/png", "image/jpeg"]:
            raise HTTPException(status_code=400, detail="Only PNG or JPG allowed")

        image_bytes = await file.read()

        if not image_bytes:
            raise HTTPException(status_code=400, detail="Empty file received")

        output = remove(image_bytes, session=session)
        return StreamingResponse(io.BytesIO(output), media_type="image/png")

    except Exception as e:
        # ⚠️ Tu peux logguer l'erreur ici
        print(f"Error in /remove-bg/: {str(e)}")
        raise HTTPException(status_code=500, detail="Background removal failed")
