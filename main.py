from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from typing import Optional, List
from PIL import Image
from PIL.ExifTags import TAGS
from io import BytesIO

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


def extract_image_metadata(image_file):
    """
    Extract metadata from an image file.

    Args:
        image_file (BytesIO): The uploaded image file in memory.

    Returns:
        dict: A dictionary of metadata tags and their values.
    """
    try:
        # Open the image file from the BytesIO stream
        with Image.open(image_file) as img:
            # Get the EXIF data
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

    except Exception as e:
        return {"error": f"An error occurred while extracting metadata: {e}"}


@app.post("/parse_receipt")
async def scan_receipt(file: UploadFile = File(...)):
    """
    Submit a receipt image to be scanned and processed.

    - **Returns**: The filename, format, and metadata of the image.
    """

    try:
        # Read the uploaded file into memory
        file_contents = await file.read()
        image_file = BytesIO(file_contents)

        # Extract metadata
        metadata = extract_image_metadata(image_file)

        # Return the filename, format, and metadata
        return {
            "filename": file.filename,
            "format": file.content_type,
            "metadata": metadata,
        }

    except Exception as e:
        return {"error": f"An error occurred while processing the file: {e}"}
