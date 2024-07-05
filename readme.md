# minimal quick label app


```bash
conda create -n quick_label_app python=3.11 -y
conda activate quick_label_app
pip install fastapi uvicorn

uvicorn main:app --reload
```