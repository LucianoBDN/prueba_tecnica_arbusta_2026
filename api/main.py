from fastapi import FastAPI
from nlp.analyzer import analyze_text, analizeCSV
from nlp.schemas import AnalyzeRequest, AnalyzeResponse
from fastapi import HTTPException


app = FastAPI()

@app.post("/analyze",    
    response_model=AnalyzeResponse,
    summary="Analiza el sentimiento del texto ingresado",
    description="devuelve la etiqueta de opinion y la puntuacion de confianza en la prediccion")
async def api_analize(data: AnalyzeRequest):
    try:
        return analyze_text(data.text)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
@app.get("/analyze-csv")
async def api_analize_csv():
    try:
        return analizeCSV(r"C:/Users/Luciano/Desktop/prueba_tecnica_arbusta_bordon_luciano\data/reviews.csv")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))