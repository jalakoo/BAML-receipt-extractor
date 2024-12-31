from fastapi import FastAPI, File, UploadFile
from baml_util import extract_receipt_from_url, extract_receipt_from_base64
import base64
import logging

app = FastAPI()


@app.post("/parse_receipt_url")
async def scan_receipt_url(url: str):
    """
    Submit a receipt image URL to be scanned and processed.

    - **Returns**: The filename, format, and metadata of the image.
    """

    try:
        output = await extract_receipt_from_url(url)
    except Exception as e:
        logging.error(e)
        return {"error": f"Failed to extract receipt from image: {e}"}
    return output


@app.post("/parse_receipt_image")
async def scan_receipt_file(file: UploadFile = File(...)):
    """
    Submit a receipt image to be scanned and processed.

    - **Returns**: The filename, format, and metadata of the image.
    """

    # Encode the image file to base64
    file_contents = await file.read()
    image_file = base64.b64encode(file_contents).decode("utf-8")

    try:
        output = await extract_receipt_from_base64(image_file)
    except Exception as e:
        logging.error(e)
        return {"error": f"Failed to extract receipt from image: {e}"}
    return output
