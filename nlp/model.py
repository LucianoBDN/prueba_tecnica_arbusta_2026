# from transformers import pipeline

# sentiment_model = pipeline(
#     "sentiment-analysis",
#     model="cardiffnlp/twitter-xlm-roberta-base-sentiment"
# )


from transformers import AutoTokenizer, AutoModelForSequenceClassification
from transformers import AutoConfig
import torch

MODEL_NAME = "cardiffnlp/twitter-xlm-roberta-base-sentiment"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)
config = AutoConfig.from_pretrained(MODEL_NAME)
