import os
from .config import UPLOAD_DIR, OUTPUT_DIR
from .converter import convert_pdf_to_word
import logging

# In-memory task status storage (Simple replacement for Redis/Celery)
task_status_store = {}

def convert_pdf_task_local(task_id, file_path, output_name):
    """Background task for PDF conversion using FastAPI BackgroundTasks."""
    output_path = os.path.join(OUTPUT_DIR, output_name)
    
    # Initialize status
    task_status_store[task_id] = {'status': 'PROCESSING', 'progress': 0}
    
    def update_progress(current):
        task_status_store[task_id]['progress'] = current
        
    try:
        success = convert_pdf_to_word(file_path, output_path, progress_callback=update_progress)
        if success:
            task_status_store[task_id] = {
                'status': 'SUCCESS', 
                'progress': 100, 
                'result': {'status': 'COMPLETED', 'output_file': output_name}
            }
        else:
            task_status_store[task_id] = {'status': 'FAILURE', 'error': 'Conversion failed'}
    except Exception as e:
        logging.error(f"Error in convert_pdf_task: {e}")
        task_status_store[task_id] = {'status': 'FAILURE', 'error': str(e)}
