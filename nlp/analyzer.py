import torch
import numpy as np
from scipy.special import softmax

from nlp.model import tokenizer, model, config


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
