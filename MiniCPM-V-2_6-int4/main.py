from transformers import AutoModel, AutoTokenizer
import logging
import os
from utils.logger import Logger  # SKIP
from utils.utils import decode_base64_to_image  # SKIP

logger_level = os.getenv("LOGGER_LEVEL", "INFO").upper()  # SKIP
log_level = getattr(logging, logger_level, logging.INFO)  # SKIP
logger = Logger(log_level).get_logger()  # SKIP


class MiniCPM_V_2_6_Int4:
    def load(self):
        self.model_name = "openbmb/MiniCPM-V-2_6-int4"
        try:
            self.model = AutoModel.from_pretrained(
                self.model_name, trust_remote_code=True
            )
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_name, trust_remote_code=True
            )
            self.model.eval()
            logger.info(f"Model {self.model_name} loaded successfully.")
        except Exception as e:
            logger.error(f"Failed to load model {self.model_name}: {str(e)}")
            raise e

    def infer(self, base64_image: str, question: str):
        try:
            image = decode_base64_to_image(base64_image)
            msgs = [{"role": "user", "content": [image, question]}]
            result = self.model.chat(image=None, msgs=msgs, tokenizer=self.tokenizer)
            logger.info("Inference completed successfully.")
            return result
        except Exception as e:
            logger.error(f"Inference failed: {str(e)}")
            raise e
