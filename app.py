from fastapi import FastAPI, File, UploadFile
from PIL import Image
import io
import cv2
import numpy as np
import easyocr
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

reader = easyocr.Reader(['en'])


def process_image(image):

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    result = reader.readtext(gray)

    extracted_text = [text for (bbox, text, prob) in result]

    return extracted_text


@app.post("/uploadfile/")
async def upload_image_and_extract_text(file: UploadFile = File(...)):

    contents = await file.read()
    image_stream = io.BytesIO(contents)
    img = Image.open(image_stream)

    img = np.array(img)

    extracted_text = process_image(img)

    return {"text": extracted_text}


@app.get("/")
async def get_status():
    return {"status": "running"}
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
