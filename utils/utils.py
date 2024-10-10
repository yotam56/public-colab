from PIL import Image
import base64
from io import BytesIO

import logging
import os
from utils.logger import Logger  # SKIP

logger_level = os.getenv("LOGGER_LEVEL", "INFO").upper()  # SKIP
log_level = getattr(logging, logger_level, logging.INFO)  # SKIP
logger = Logger(log_level).get_logger()  # SKIP


def decode_base64_to_image(image_base64: str) -> Image.Image:
    try:
        image_data = base64.b64decode(image_base64)
        image = Image.open(BytesIO(image_data)).convert("RGB")
        logger.info("Image decoded successfully")
        return image
    except Exception as e:
        print(f"Error decoding base64 image: {str(e)}")
        raise
