from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import nest_asyncio
from pyngrok import ngrok
import uvicorn
import logging
import os
from utils.logger import Logger  # SKIP
from main import MiniCPM_V_2_6_Int4  # SKIP

logger_level = os.getenv("LOGGER_LEVEL", "INFO").upper()  # SKIP
log_level = getattr(logging, logger_level, logging.INFO)  # SKIP
logger = Logger(log_level).get_logger()  # SKIP

app = FastAPI()
model_instance = MiniCPM_V_2_6_Int4()
model_instance.load()


class MultimodalRequest(BaseModel):
    question: str
    base64_image: str


class MultimodalResponse(BaseModel):
    prediction: str


@app.get("/health_check")
async def health_check():
    logger.info("Health check called.")
    return {"status": "Healthy"}


@app.post("/infer")
async def infer(infer_request: MultimodalRequest):
    try:
        logger.info("Received inference request.")
        prediction = model_instance.infer(
            infer_request.base64_image, infer_request.question
        )
        logger.info("Returning inference result.")
        return MultimodalResponse(prediction=prediction)
    except Exception as e:
        logger.error(f"Error during inference request: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# Connect to ngrok on Colab
ngrok_tunnel = ngrok.connect("9200")
print("Public URL:", ngrok_tunnel.public_url)

# Apply nest_asyncio to allow nested event loops
nest_asyncio.apply()

# Function to forward requests from Colab to your local server


if __name__ == "__main__":
    logger.info("Starting the Uvicorn server...")
    uvicorn.run(app, host="0.0.0.0", port=9200)
    logger.info("Server has started.")
