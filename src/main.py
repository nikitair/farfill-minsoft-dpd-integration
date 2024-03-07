from fastapi import FastAPI
import uvicorn
from logs.logging_config import logger


app = FastAPI()


@app.get("/")
def index():
    logger.info(f"{index.__name__} -- INDEX ENDPOINT TRIGGERED")
    return {"message": "Hello World!"}


if __name__ =="__main__":
    uvicorn.run(app=app, port=8000, host="0.0.0.0")

