from baml_py import Image
from baml_client import b
from dotenv import load_dotenv

# LLM API Keys are located in the .env file
load_dotenv()


async def extract_receipt_from_url(url: str):
    """
    Extracts an image of a receipt stored at a URL.

    Args:
        url (str): The URL of the receipt image.

    Returns:
        dict: The receipt data. See the baml_src/recipt_model.baml file for the structure of the receipt data.

    Raises:
        BamlValidationError: If the llm read of the image could not be parsed into the expected data model.
    """
    img = Image.from_url(url)
    output = b.ExtractReceiptFromImage(img)
    return output


async def extract_receipt_from_base64(base64: str):
    """Extract a receipt from a base 64 image file.

    Args:
        base64 (str): Base64 string encoded image

    Returns:
        dict: The receipt data. See the baml_src/recipt_model.baml file for the structure of the receipt data.

    Raises:
        BamlValidationError: If the llm read of the image could not be parsed into the expected data model.
    """

    img_64 = Image.from_base64("image/png", base64)
    output = b.ExtractReceiptFromImage(img_64)
    return output
