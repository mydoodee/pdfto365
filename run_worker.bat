@echo off
echo Starting PDF-TO365 Celery Worker (Processing Engine)...
echo Mode: Windows Solo Pool (Eventlet/Solo recommended for Windows)
python -m celery -A backend.tasks worker --loglevel=info -P solo
pause
