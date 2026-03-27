@echo off
echo ==========================================
echo  PDF-TO365 — ระบบติดตั้งสำหรับเครื่องใหม่
echo ==========================================
echo.
echo 1. กำลังตรวจสอบ Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] ไม่พบ Python ในเครื่องนี้! กรุณาติดตั้ง Python 3.10+ ก่อนรันครับ
    pause
    exit /b
)

echo 2. กำลังติดตั้ง Library ที่จำเป็น...
pip install -r backend/requirements.txt

echo 3. ตรวจสอบ Tesseract-OCR...
if not exist "C:\Program Files\Tesseract-OCR\tesseract.exe" (
    echo.
    echo [คำเตือน] ไม่พบ Tesseract-OCR ในตำแหน่งมาตรฐาน!
    echo อย่าลืมติดตั้ง Tesseract-OCR พร้อมภาษาไทย (Thai) ด้วยนะครับ
    echo ดาวน์โหลดได้ที่: https://github.com/UB-Mannheim/tesseract/wiki
)

echo.
echo ==========================================
echo  [สำเร็จ] ติดตั้งเรียบร้อยแล้ว! พร้อมใช้งาน
echo  รันโปรแกรมด้วยไฟล์: run_dev.bat
echo ==========================================
pause
