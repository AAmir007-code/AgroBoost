import os
import boto3
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from segment_anything import SamPredictor, sam_model_registry
import cv2
import numpy as np
import requests

app = FastAPI()

# MinIO configuration
MINIO_URL = "http://minio:9000"  # Adjust according to your setup
MINIO_BUCKET = "images"
MINIO_ACCESS_KEY = "your_access_key"
MINIO_SECRET_KEY = "your_secret_key"

# Backend URL for sending results
BACKEND_URL = "http://api.ecomobile.uz/api/results"

# Initialize MinIO client
s3_client = boto3.client('s3', endpoint_url=MINIO_URL,
                          aws_access_key_id=MINIO_ACCESS_KEY,
                          aws_secret_access_key=MINIO_SECRET_KEY)

# Load SAM model
MODEL_TYPE = "vit_h"
sam_checkpoint = os.path.join("models", f"sam_{MODEL_TYPE}.pth")
sam = sam_model_registry[MODEL_TYPE](checkpoint=sam_checkpoint)
predictor = SamPredictor(sam)

class InferenceResult(BaseModel):
    filename: str
    result: str

@app.post("api/upload/")
async def upload_image(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        file_name = file.filename

        # Save to MinIO
        s3_client.put_object(Bucket=MINIO_BUCKET, Key=file_name, Body=contents)
        return JSONResponse(content={"message": "Image uploaded successfully."})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("api/process/")
async def process_images():
    try:
        # List all images in the bucket
        objects = s3_client.list_objects_v2(Bucket=MINIO_BUCKET)
        results = []

        for obj in objects.get('Contents', []):
            file_name = obj['Key']

            # Download image from MinIO
            image_obj = s3_client.get_object(Bucket=MINIO_BUCKET, Key=file_name)
            image_data = image_obj['Body'].read()
            nparr = np.frombuffer(image_data, np.uint8)
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            # Perform inference (use your bbox logic here)
            bbox = (50, 50, 600, 400)  # Example bounding box
            mask = segment_frame(predictor, image, bbox)

            # Save or process the mask as needed
            result_text = f"Processed {file_name}"
            results.append(InferenceResult(filename=file_name, result=result_text))

            # Send results to another backend
            requests.post(BACKEND_URL, json={"filename": file_name, "result": result_text})

        return JSONResponse(content={"results": [result.dict() for result in results]})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def segment_frame(predictor, frame, bbox):
    input_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB).astype(np.float32) / 255.0
    predictor.set_image(input_frame)
    masks, _, _ = predictor.predict(boxes=np.array([bbox]), multimask_output=False)
    return masks[0]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)