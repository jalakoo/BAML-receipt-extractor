from PIL import Image as PILImage
from PIL.ExifTags import TAGS
from io import BytesIO
from baml_py import Image
from baml_client import b
from dotenv import load_dotenv
import base64

# LLM API Keys are located in the .env file
load_dotenv()


async def extract_receipt_from_url(url: str):
    """
    Extracts the receipt from the given URL.

    Args:
        url (str): The URL of the receipt image.

    Returns:
        dict: The receipt data. See the baml_src/recipt_model.baml file for the structure of the receipt data.
    """
    img = Image.from_url(url)
    output = b.ExtractReceiptFromImage(img)
    return output


async def extract_receipt_from_image(image_file: BytesIO):
    """Extract a reeceipt from a base 64 image file.

    Args:
        image_file (bytes): Image as BytesIO object.

    Returns:
        dict: The receipt data. See the baml_src/recipt_model.baml file for the structure of the receipt data.
    """

    try:
        # Read the uploaded file into memory
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
