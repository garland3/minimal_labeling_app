import json
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import json
import os
from pathlib import Path

app = FastAPI()
coordinates = []

# make dir output
os.makedirs("output", exist_ok=True)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Specify the image directory
IMG_DIR = Path("my_cool_imgs")  # Replace with your actual image directory path

# Get a list of all image files in the directory
image_files = sorted([str(file.relative_to(IMG_DIR)) for file in IMG_DIR.glob("*") if file.suffix.lower() in ['.jpg', '.jpeg', '.png', '.gif']])

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    if image_files:
        return templates.TemplateResponse("index.html", {"request": request, "img_file_path": f"/images/{image_files[0]}"})
    else:
        return templates.TemplateResponse("index.html", {"request": request, "img_file_path": ""})

@app.get("/get_image/{index}")
async def get_image(index: int):
    if 0 <= index < len(image_files):
        return {"img_file_path": f"/images/{image_files[index]}"}
    else:
        return {"error": "Image index out of range"}

@app.get("/image_count")
async def get_image_count():
    return {"count": len(image_files)}

# Mount the image directory
app.mount("/images", StaticFiles(directory=IMG_DIR), name="images")



@app.post("/submit_coordinates")
async def submit_coordinates(request: Request):
    data = await request.json()
    currentImageIndex = int(data['currentImageIndex'])
    # Append coordinates to list
    # coordinates.extend(data['coordinates'])
    
    # Save coordinates to file as JSON
    filename = f"output/coordinates_{currentImageIndex}.json"
    with open(filename, 'w') as f:
        json.dump(coordinates, f, indent=2)
    
    return {"message": "Coordinates received and stored"}



@app.get("/get_coordinates")
async def get_coordinates():
    return {"coordinates": coordinates}