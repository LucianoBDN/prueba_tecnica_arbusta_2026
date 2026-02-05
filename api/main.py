from fastapi import FastAPI
from nlp.analyzer import analyze_text

app = FastAPI()

@app.post("/analyze")
async def api_analize(data: dict):
    result = analyze_text(data["text"])
    return result