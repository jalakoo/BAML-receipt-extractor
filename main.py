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


def extract_metadata_from_img(img):
    exif_data = img.getexif()
    if not exif_data:
        return {"error": "No EXIF metadata found in the image."}

    # Translate the EXIF tag IDs to their names
    metadata = {}
    for tag_id, value in exif_data.items():
        tag_name = TAGS.get(tag_id, tag_id)

        # Convert IFDRational or other non-serializable types to strings
        if isinstance(value, bytes):
            value = value.decode(errors="ignore")  # Decode bytes to string
        elif isinstance(value, tuple):
            value = tuple(map(str, value))  # Convert tuple elements to strings
        else:
            value = str(value)

        metadata[tag_name] = value

    return metadata


# @app.post("/parse_receipt_url")
# async def scan_receipt_url(url: str):
#     """
#     Submit a receipt image URL to be scanned and processed.

#     - **Returns**: The filename, format, and metadata of the image.
#     """


@app.post("/parse_receipt")
async def scan_receipt_file(file: UploadFile = File(...)):
    """
    Submit a receipt image to be scanned and processed.

    - **Returns**: The filename, format, and metadata of the image.
    """

    key = os.getenv("OPENAI_API_KEY")
    if not key:
        return {"error": "OPENAI_API_KEY not found in environment variables."}

    try:
        # Read the uploaded file into memory
        file_contents = await file.read()
        image_file = BytesIO(file_contents)

        # Extract metadata
        # metadata = extract_image_metadata(image_file)

        # Extract details using BAML
        with PILImage.open(image_file) as img:

            metadata = extract_metadata_from_img(img)

            buffered = BytesIO()
            img.save(buffered, format="PNG")
            img_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

            img_64 = Image.from_base64("image/png", img_base64)
            output = b.ExtractReceiptFromImage(img_64)

            # Return the filename, format, and metadata
            return {
                "filename": file.filename,
                "format": file.content_type,
                "metadata": metadata,
                "receipt_data": output,
            }

    except Exception as e:
        return {"error": f"An error occurred while processing the file: {e}"}
