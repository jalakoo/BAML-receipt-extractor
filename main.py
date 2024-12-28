from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from typing import Optional, List
from PIL import Image as PILImage
from PIL.ExifTags import TAGS
from io import BytesIO
from baml_py import Image
from baml_client import b
from dotenv import load_dotenv
import os
import base64

load_dotenv()
app = FastAPI()


class ReceiptItem(BaseModel):
    description: str
    quantity: int
    price: float


class Receipt(BaseModel):
    items: List[ReceiptItem]
    total_amount: float
    date: str
    vendor: str
    address: Optional[str]


@app.post("/parse_receipt_url")
async def scan_receipt_url(url: str):
    """
    Submit a receipt image URL to be scanned and processed.

    - **Returns**: The filename, format, and metadata of the image.
    """

    img = Image.from_url(url)
    output = b.ExtractReceiptFromImage(img)
    return output


@app.post("/parse_receipt_image")
async def scan_receipt_file(file: UploadFile = File(...)):
    """
    Submit a receipt image to be scanned and processed.

    - **Returns**: The filename, format, and metadata of the image.
    """

    try:
        # Read the uploaded file into memory
        file_contents = await file.read()
        image_file = BytesIO(file_contents)

        # Extract details using BAML
        with PILImage.open(image_file) as img:

            # Need to convert to base64 to pass to BAML
            buffered = BytesIO()
            img.save(buffered, format="PNG")
            img_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

            img_64 = Image.from_base64("image/png", img_base64)
            output = b.ExtractReceiptFromImage(img_64)

            # Return output as JSON
            return output

    except Exception as e:
        return {"error": f"An error occurred while processing the file: {e}"}
