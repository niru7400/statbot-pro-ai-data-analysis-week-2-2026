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

# graph folder serve
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


# 📂 Upload
@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    global agent

    path = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    agent = create_agent(path)

    return RedirectResponse(url="/", status_code=303)


# 🤖 Ask
@app.get("/ask", response_class=HTMLResponse)
def ask(request: Request, q: str):
    global agent

    if agent is None:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "result": "Upload CSV first ❌"
        })

    try:
        # GRAPH KEYWORDS DETECTION
        graph_keywords = ["plot", "graph", "chart", "visualize"]

        if any(word in q.lower() for word in graph_keywords):
            prompt = q + " using matplotlib and save plot"
            is_graph = True
        else:
            prompt = q + " give only final short answer in one line. no explanation."
            is_graph = False

        result = agent.invoke(prompt)

        # CLEAN OUTPUT
        if isinstance(result, dict):
            result = result.get("output", str(result))

        #  GRAPH ONLY WHEN NEEDED
        image_path = None
        if is_graph:
            files = os.listdir("graph")
            if files:
                latest = sorted(files)[-1]
                image_path = "graph/" + latest

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