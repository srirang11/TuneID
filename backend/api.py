from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import tempfile
from app.matcher import identify

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/identify")
async def identify_song(file: UploadFile = File(...)):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            tmp.write(await file.read())
            path = tmp.name

        result = identify(path)
        return result or {"song": None, "score": 0}

    except Exception as e:
        print("ERROR IN /identify:", e)
        raise e
