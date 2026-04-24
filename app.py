from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from services.ml_service.src.main import app as api_app

app = FastAPI()

app.mount("/api", api_app)

app.mount(
    "/",
    StaticFiles(directory="resumelens-ui/dist", html=True),
    name="static",
)

@app.get("/")
def serve_react():
    return FileResponse("resumelens-ui/dist/index.html")    