from fastapi import FastAPI

app = FastAPI(title="DeepSeek-V3 Chat API")

@app.get("/")
def root():
    return {"message": "DeepSeek-V3 Chat API is running"}

# Запуск: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
