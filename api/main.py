from fastapi import FastAPI, Query, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from nlp.analyzer import analyze_text, analizeCSV
from nlp.schemas import AnalyzeRequest, AnalyzeResponse
import tempfile
import shutil


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:4200",   # Angular
        "http://127.0.0.1:4200"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/analyze",    
    response_model=AnalyzeResponse,
    summary="Analiza el sentimiento del texto ingresado",
    description="devuelve la etiqueta de opinion y la puntuacion de confianza en la prediccion")
async def api_analize(data: AnalyzeRequest):
    try:
        return analyze_text(data.text)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
        
@app.post("/analyze-csv",
    summary="Analiza un archivo CSV con múltiples textos",
    description=(
        "Recibe un archivo CSV con columnas `id` y `message`, analiza el "
        "sentimiento de los textos usando un modelo Transformer preentrenado "
        "y devuelve los resultados de forma paginada."
        "Query params:"
        "- page: número de página (base 1)"
        "- page_size: cantidad de registros por página"
        "La respuesta incluye metadata de paginación y los resultados "
        "de sentimiento para la página solicitada."
    )
)
async def api_analyze_csv_upload(file: UploadFile = File(...),
            page: int = Query(1, ge=1),
            page_size: int = Query(10, ge=1, le=100)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="El archivo debe ser CSV")

    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp:
        shutil.copyfileobj(file.file, tmp)
        temp_path = tmp.name

    try:
        return analizeCSV(
            temp_path,
            page=page,
            page_size=page_size)
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))