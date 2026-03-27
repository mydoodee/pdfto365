import os
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_DIR = BASE_DIR / "uploads"
OUTPUT_DIR = BASE_DIR / "outputs"
FONTS_DIR = BASE_DIR / "fonts"

# Ensure directories exist
for d in [UPLOAD_DIR, OUTPUT_DIR, FONTS_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# Redis & Celery Config
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# Thai Font Config
THAI_FONT_NAME = "TH Sarabun New"
THAI_FONT_PATH = str(FONTS_DIR / "THSarabunNew.ttf")

# Conversion limits
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
CLEANUP_HOURS = 1
