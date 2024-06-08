from fastapi import FastAPI
from fastapi.responses import JSONResponse
from PIL import Image
import io
import requests
from ultralytics import YOLO
import asyncio

app = FastAPI()

# Load YOLOv8 model
model = YOLO("yolov8n.pt")

# Shared state for storing the head count
head_count = {"count": 0}

async def update_head_count(url: str, interval: int):
    global head_count
    while True:
        try:
            response = requests.get(url)
            img = Image.open(io.BytesIO(response.content))

            # Perform inference
            results = model(img)
            print(results)

            # Extract the number of people (class label 0 typically represents 'person' in COCO dataset)
            new_head_count = 0
            for result in results:
                for box in result.boxes:
                    if box.cls == 0:  # '0' is the class ID for 'person'
                        new_head_count += 1

            # Update the shared head count
            head_count["count"] = new_head_count

        except Exception as e:
            print(f"Error updating head count: {e}")

        await asyncio.sleep(interval)

@app.on_event("startup")
async def startup_event():
    # Start the periodic head count update task
    url = "http://192.168.7.13/capture"
    interval = 10  # seconds
    asyncio.create_task(update_head_count(url, interval))

@app.get("/predict/")
async def predict():
    # Return the current head count
    return JSONResponse(content={"head_count": head_count["count"]})

# Run the app with: uvicorn main2:app --reload
