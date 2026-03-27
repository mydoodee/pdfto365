from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
import uuid
import shutil
from .config import UPLOAD_DIR, OUTPUT_DIR, MAX_FILE_SIZE
from .tasks import convert_pdf_task_local, task_status_store

app = FastAPI(title="PDF-TO365 API")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files for frontend
if os.path.exists("frontend"):
    app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.post("/api/upload")
async def upload_pdf(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    """Upload PDF and start conversion task (FastAPI Background)."""
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    file_id = str(uuid.uuid4())
    temp_filename = f"{file_id}.pdf"
    file_path = os.path.join(UPLOAD_DIR, temp_filename)
    
    # Initialize initial state
    task_status_store[file_id] = {'status': 'PENDING', 'progress': 0}
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    # Start background task WITHOUT Celery
    output_filename = f"{file_id}.docx"
    background_tasks.add_task(convert_pdf_task_local, file_id, file_path, output_filename)
    
    return {
        "task_id": file_id,
        "filename": file.filename,
        "status": "QUEUED"
    }

@app.get("/api/status/{task_id}")
async def get_status(task_id: str):
    """Check task status and progress (from internal dictionary)."""
    task_data = task_status_store.get(task_id)
    
    if not task_data:
        return {"status": "NOT_FOUND", "progress": 0}
        
    return task_data

@app.get("/api/download/{task_id}")
async def download_file(task_id: str):
    """Download the converted Word file."""
    output_filename = f"{task_id}.docx"
    file_path = os.path.join(OUTPUT_DIR, output_filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found or not yet processed")
        
    return FileResponse(
        path=file_path,
        filename="converted_thai_pdf.docx",
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )

@app.get("/")
async def root():
    """Serve the frontend entry point."""
    index_path = os.path.join("frontend", "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "PDF-TO365 API is running. No frontend found in /frontend folder."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
