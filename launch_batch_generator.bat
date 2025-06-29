@echo off
cd /d %~dp0
call venv\Scripts\activate.bat

IF NOT EXIST .env (
    echo OPENAI_API_KEY=your-api-key-here > .env
)

echo Launching Batch Generator...
streamlit run batch_generator.py
pause
