
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from transformers import AutoConfig
import torch

# Nombre del modelo preentrenado que uso
MODEL_NAME = "cardiffnlp/twitter-xlm-roberta-base-sentiment"

# Cargar el tokenizador correspondiente al modelo
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

# Cargar el modelo de clasificación de secuencias
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)

# Cargar la configuración del modelo
config = AutoConfig.from_pretrained(MODEL_NAME)
