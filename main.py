import json
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, HTMLResponse
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

# Mount the image directory
app.mount("/images", StaticFiles(directory=IMG_DIR), name="images")

# Get a list of all image files in the directory
image_files = sorted([str(file.relative_to(IMG_DIR)) for file in IMG_DIR.glob("*") if file.suffix.lower() in ['.jpg', '.jpeg', '.png', '.gif']])

output_dir = Path("output")
output_dir.mkdir(parents=True, exist_ok=True)
# mount the output directory
app.mount("/output", StaticFiles(directory=output_dir), name="output")

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




@app.post("/submit_coordinates")
async def submit_coordinates(request: Request):
    data = await request.json()
    print("data", data)
    currentImageIndex = int(data['currentImageIndex'])
    # add the idx and fielname to the data dict
    data['idx'] = currentImageIndex
    data['filename'] = image_files[currentImageIndex]    
    # Save coordinates to file as JSON
    filename = output_dir/f"coordinates_{currentImageIndex}.json"
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    return {"message": "Coordinates received and stored"}

# show all the output files togehter
# combine all into one json file. 
# make a download button that downloads the json file
file_path_combined_json = output_dir/"combined.json"
def combine_files():
    # json_files = sorted([str(file.relative_to(output_dir)) for file in output_dir.glob("coordinates_*") if file.suffix.lower() == '.json'])
    json_files = list(output_dir.glob("coordinates_*"))
    combined_dict =[]
    for j in json_files:
        with open(j) as f:
            data = json.load(f)
            combined_dict.append(data)
    # save the combined dict to a file
    # with open(output_dir/"combined.json", 'w') as f:
    with open(file_path_combined_json, 'w') as f:
        json.dump(combined_dict, f, indent=2)
    return combined_dict

@app.get("/download")
async def download():
    # read the json files
    combine_files()
    return FileResponse(file_path_combined_json, media_type="application/json", filename=f"combined.json")

# view the combined files, but wrapped in a simple html page
# at /download_view
@app.get("/download_view")
async def download_view():
    myjson = combine_files()
    return HTMLResponse( f""" 
    <html>
        <body>
            {json.dumps(myjson, indent=2)}
        </body>
    </html>
    """)


@app.get("/get_coordinates")
async def get_coordinates():
    return {"coordinates": coordinates}