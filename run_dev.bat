@echo off
echo Starting PDF-TO365 All-in-One Engine...
echo System: FastAPI BackgroundTasks (No Redis Required)
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
pause
