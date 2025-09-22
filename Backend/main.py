from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import numpy as np
from PIL import Image
import io
import os
import traceback
from model.model_loader import ecoscan_model

app = FastAPI(title="EcoScan API", description="API for waste material classification")

origins = [
    "https://ecoscan-backend.onrender.com"
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs("temp_uploads", exist_ok=True)

@app.get("/")
async def root():
    return {"message": "EcoScan API is running!", "status": "success"}

@app.get("/classes")
async def get_classes():
    return {
        "classes": ecoscan_model.class_labels,
        "count": len(ecoscan_model.class_labels)
    }

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        if file.content_type and not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        allowed_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp'}
        file_extension = os.path.splitext(file.filename.lower())[1]
        if file_extension not in allowed_extensions:
            raise HTTPException(status_code=400, detail="File must be an image (jpg, png, etc.)")
        
        contents = await file.read()
        
        try:
            image = Image.open(io.BytesIO(contents)).convert('RGB')
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid image file: {str(e)}")
        
        image = image.resize((128, 128))
        
        image_array = np.array(image)
        
        result = ecoscan_model.predict_image(image_array)
        
        material_info = {
            "plastic": "Recyclable - Check local recycling guidelines",
            "paper": "Recyclable - Should be clean and dry",
            "cardboard": "Recyclable - Flatten before recycling",
            "metal": "Recyclable - Rinse before recycling",
            "glass": "Recyclable - Separate by color if required",
            "battery": "Hazardous - Dispose at proper collection points",
            "biological": "Compostable - Can be composted if organic",
            "clothes": "Donatable - Consider donating if in good condition",
            "shoes": "Donatable - Consider donating if wearable",
            "trash": "General waste - Dispose in regular trash"
        }
        
        advice = material_info.get(
            result["predicted_class"].lower(), 
            "Check local waste management guidelines"
        )
        
        response = {
            "status": "success",
            "prediction": result["predicted_class"],
            "confidence": result["confidence"],
            "advice": advice,
            "all_predictions": result["all_predictions"]
        }
        
        return JSONResponse(content=response)
        
    except HTTPException:
        raise
    except Exception as e:
        error_msg = f"Error processing image: {str(e)}"
        print(error_msg)
        print("Full traceback:")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=error_msg)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)