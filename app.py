from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import shutil
import os

from agent import create_agent

app = FastAPI()

# Templates
templates = Jinja2Templates(directory="templates")

# graph folder
os.makedirs("graph", exist_ok=True)
app.mount("/graph", StaticFiles(directory="graph"), name="graph")

# Upload folder
UPLOAD_FOLDER = "data"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

agent = None


# 🏠 Home
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# 📂 Upload CSV
@app.post("/upload")
async def upload(request: Request, file: UploadFile = File(...)):
    global agent

    path = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    agent = create_agent(path)

    return templates.TemplateResponse("index.html", {
        "request": request,
        "msg": f"✅ {file.filename} uploaded successfully!"
    })

# 🤖 Ask Question
@app.get("/ask", response_class=HTMLResponse)
def ask(request: Request, q: str):
    global agent

    if agent is None:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "result": "Upload CSV first ❌"
        })

    try:
        result = agent(q)   # 🔥 NEW (no invoke)

        image_path = None

        # 🔥 If result is graph file
        if isinstance(result, str) and result.startswith("graph/"):
            image_path = result
            result = "Graph generated ✅"

        return templates.TemplateResponse("index.html", {
            "request": request,
            "result": result,
            "image": image_path
        })

    except Exception as e:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "result": str(e)
        })