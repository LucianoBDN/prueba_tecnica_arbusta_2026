from fastapi import FastAPI, UploadFile, File, HTTPException
from nlp.analyzer import analyze_text, analizeCSV
from nlp.schemas import AnalyzeRequest, AnalyzeResponse
import tempfile
import shutil


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
        return analizeCSV(r"./data/reviews.csv")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.post("/analyze-csv-upload",
    summary="Analiza un archivo CSV con múltiples textos",
    description=(
        "Recibe un archivo CSV con una columna `message` y devuelve, "
        "para cada fila, el sentimiento detectado y el score de confianza "
        "utilizando un modelo Transformer preentrenado."
    )
)
async def api_analyze_csv_upload(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="El archivo debe ser CSV")

    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp:
        shutil.copyfileobj(file.file, tmp)
        temp_path = tmp.name

    try:
        return analizeCSV(temp_path)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))