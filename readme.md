# minimal quick label app

Put your images in 
`my_cool_imgs` folder and run the app.

will give you json output of the bounding box.


```bash
conda create -n quick_label_app python=3.11 -y
conda activate quick_label_app
pip install fastapi uvicorn

uvicorn main:app --reload
```

## Screen shot video.

[![BBox GIF](readme_imgs/bbox.gif)](readme_imgs/bbox.gif)


