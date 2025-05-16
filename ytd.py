from fastapi import FastAPI, Form, BackgroundTasks
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import yt_dlp
import uuid
import os
from pathlib import Path

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

DOWNLOAD_DIR = str(Path.home() / "Downloads")

def cleanup_file(file_path: str):
    try:
        os.remove(file_path)
        print(f"File {file_path} dihapus")
    except Exception as e:
        print(f"Gagal menghapus file: {e}")

@app.post("/info")
async def get_info(url: str = Form(...)):
    try:
        ydl_opts = {"quiet": True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return {
                "title": info.get("title"),
                "thumbnail": info.get("thumbnail"),
            }
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})

@app.post("/download")
def download_video(
    background_tasks: BackgroundTasks,
    url: str = Form(...),
    resolution: str = Form(...)
):
    unique_filename = f"{uuid.uuid4()}.mp4"
    full_path = os.path.join(DOWNLOAD_DIR, unique_filename)

    ydl_opts = {
        "format": f"bestvideo[height={resolution}]+bestaudio/best",
        "merge_output_format": "mp4",
        "outtmpl": full_path,
        "quiet": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    background_tasks.add_task(cleanup_file, full_path)
    return FileResponse(full_path, media_type="video/mp4", filename=unique_filename)
