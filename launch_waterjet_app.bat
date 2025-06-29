@echo off
REM Activate virtual environment and launch Streamlit app

cd /d %~dp0
call venv\Scripts\activate.bat

REM Set your OpenAI key if not already in .env
IF NOT EXIST .env (
    echo OPENAI_API_KEY=your-api-key-here > .env
)

echo Starting Waterjet AI App...
streamlit run app.py
pause
