from fastapi import FastAPI, Body
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from PIL import Image
import io
import requests
from ultralytics import YOLO
import asyncio
import base64
import httpx

app = FastAPI()

# Load YOLOv8 model
model = YOLO("yolov8n.pt")

# Shared state for storing the head count and sensor data
head_count = {"count": 0}
img_arr = []

# Supabase configuration
SUPABASE_URL = "https://gwyyixagttragoezrbub.supabase.co"
SUPABASE_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imd3eXlpeGFndHRyYWdvZXpyYnViIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTc4Njg3MzEsImV4cCI6MjAzMzQ0NDczMX0.52qJhOCoGnNFxLwArSj0C1CXV4CcptpIAphwsUEzc4k"
SUPABASE_TABLE = "person_counter"

async def update_head_count(url: str, interval: int):
    global head_count
    global img_arr
    while True:
        try:
            response = requests.get(url)
            img = Image.open(io.BytesIO(response.content))

            # Perform inference
            results = model(img)

            # Extract the number of people (class label 0 typically represents 'person' in COCO dataset)
            new_head_count = 0
            for result in results:
                for box in result.boxes:
                    if box.cls == 0:  # '0' is the class ID for 'person'
                        new_head_count += 1

            # Update the shared head count
            head_count["count"] = new_head_count

            # Convert the image to base64
            for result in results:
                imgs = Image.fromarray(result.orig_img)
                imgs_bytes = io.BytesIO()
                imgs.save(imgs_bytes, format="JPEG")
                imgs_base64 = base64.b64encode(imgs_bytes.getvalue()).decode("utf-8")
                img_arr.append(imgs_base64)

            # Prepare the payload for Supabase
            payload = {
                "head_count": new_head_count,
                "img_string_base64": imgs_base64,  # Use the latest image
                "mosque_id": 1
            }

            # Send data to Supabase
            async with httpx.AsyncClient() as client:
                headers = {
                    "Content-Type": "application/json",
                    "apikey": SUPABASE_API_KEY,
                    "Authorization": f"Bearer {SUPABASE_API_KEY}"
                }
                supabase_response = await client.post(f"{SUPABASE_URL}/rest/v1/{SUPABASE_TABLE}", headers=headers, json=payload)
                if supabase_response.status_code == 201:
                    print("Data successfully posted to Supabase")
                else:
                    print(f"Failed to post data to Supabase: {supabase_response.status_code}, {supabase_response.text}")

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
    # Return the current head count and sensor data
    return JSONResponse(content={"head_count": head_count["count"], "image": img_arr})

# run the service using : uvicorn main:app --reload