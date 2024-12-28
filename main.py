from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from typing import Optional, List
from baml_util import extract_receipt_from_url, extract_receipt_from_image
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


@app.post("/parse_receipt_url")
async def scan_receipt_url(url: str):
    """
    Submit a receipt image URL to be scanned and processed.

    - **Returns**: The filename, format, and metadata of the image.
    """

    output = await extract_receipt_from_url(url)
    return output


@app.post("/parse_receipt_image")
async def scan_receipt_file(file: UploadFile = File(...)):
    """
    Submit a receipt image to be scanned and processed.

    - **Returns**: The filename, format, and metadata of the image.
    """

    file_contents = await file.read()
    image_file = BytesIO(file_contents)
    output = await extract_receipt_from_image(image_file)
    return output
