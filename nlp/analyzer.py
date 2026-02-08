import torch
import numpy as np
from scipy.special import softmax
import pandas as pd
from nlp.model import tokenizer, model, config
from utils.file_validation import validate_csv_structure, validate_file_path, normalize_columns



def analyze_text(text: str) -> dict:
    """
    Analiza el sentimiento de un texto y devuelve
    el label predicho junto con un score de confianza.
    """
    #Validacion de que el texto no venga vacio
    if not text or not text.strip():
        raise ValueError("El texto no puede estar vacío")

    #Tokenización del texto
    encoded_input = tokenizer(
        text,
        return_tensors="pt",
        truncation=True
    )

    #Inferencia (no calcula gradientes)
    with torch.no_grad():
        output = model(**encoded_input)

    #Extracción de logits
    logits = output.logits[0].numpy()

    #Conversión a probabilidades
    scores = softmax(logits)

    #Selección del label con mayor probabilidad
    max_index = int(np.argmax(scores))

    return {
        "sentiment": config.id2label[max_index],
        "score": float(scores[max_index])
    }


def analizeCSV(path: str, page: int = 1, page_size: int =10) -> dict:
    """
    Analiza los sentimientos de los mensajes en un archivo CSV.

    Esta función toma un archivo CSV que contiene mensajes y realiza una serie de operaciones:
    1. Valida la ruta del archivo.
    2. Lee el archivo CSV en un DataFrame.
    3. Normaliza los nombres de las columnas del DataFrame.
    4. Verifica que el DataFrame contenga las columnas necesarias: 'id' y 'message'.
    5. Aplica paginación sobre los registros.
    6. Analiza el sentimiento SOLO de los mensajes de la página solicitada.
    7. Devuelve los resultados junto con metadata de paginación.

    Args:
        path (str): La ruta del archivo CSV que contiene los mensajes a analizar.
        page (int, optional): Número de página a devolver (base 1).
            Default = 1.
        page_size (int, optional): Cantidad de registros por página.
            Default = 10.
    Returns:
        dict: Objeto con metadata de paginación y resultados:
            - page (int): Página actual.
            - page_size (int): Cantidad de registros por página.
            - total_items (int): Total de registros en el CSV.
            - total_pages (int): Total de páginas disponibles.
            - data (list[dict]): Lista de resultados de sentimiento:
                - id: Identificador del mensaje.
                - message: Texto analizado.
                - sentiment: Sentimiento predicho.
                - score: Confianza de la predicción.

    Raises:
        ValueError: Si el archivo CSV tiene una estructura incorrecta o faltan columnas requeridas.
        FileNotFoundError: Si el archivo no existe en la ruta especificada.
    """ 
    validate_file_path(path)

    df = pd.read_csv(path)
    df = normalize_columns(df)

    validate_csv_structure(df, {"id", "message"})
    
    total = len(df)

    
    start = (page - 1) * page_size
    end = start + page_size

    
    page_df = df.iloc[start:end]

    results = []

    for _, row in page_df.iterrows():
        analysis = analyze_text(row["message"])
        results.append({
            "id": row["id"],
            "message": row["message"],
            "sentiment": analysis["sentiment"],
            "score": analysis["score"]
        })

    return {
        "page": page,
        "page_size": page_size,
        "total_items": total,
        "total_pages": (total + page_size - 1) // page_size,
        "data": results
    }



