from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from PIL import Image
#import torch
import io
import requests
from ultralytics import YOLO

app = FastAPI()

# Load YOLOv8 model (adjust the method according to YOLOv8 implementation)
#model = torch.hub.load('ultralytics/yolov8', 'yolov8s')  # or 'yolov8m', 'yolov8l', 'yolov8x'
model = YOLO("yolov8n.pt")

@app.get("/predict/")
async def predict(url: str):
    response = requests.get(url)
    img = Image.open(io.BytesIO(response.content))

    # Perform inference
    results = model(img)
    print(results)

    # Extract the number of people (class label 0 typically represents 'person' in COCO dataset)
    head_count = 0
    for result in results:
        for box in result.boxes:
            if box.cls == 0:  # '0' is the class ID for 'person'
                head_count += 1
                
    return JSONResponse(content={"head_count": head_count})

# Run the app with: uvicorn main:app --reload
