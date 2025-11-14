# llm_relationship.py
from typing import List, Dict
from transformers import AutoTokenizer, AutoModelForSequenceClassification, TextClassificationPipeline
import torch

# Labels you'll eventually fine-tune:
LABELS = ["friend", "partner", "family", "colleague", "acquaintance", "unknown"]

class RelationshipClassifier:
    def __init__(self):
        model_name = "distilbert-base-uncased"
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(
            model_name, num_labels=len(LABELS)
        )
        self.pipeline = TextClassificationPipeline(
            model=self.model,
            tokenizer=self.tokenizer,
            device = "mps" if torch.backends.mps.is_available() else "cpu",
            return_all_scores=True,
        )

    def classify(self, messages: List[str]) -> Dict:
        text = "\n".join(messages[-50:])  # condensed history window
        scores = self.pipeline(text)[0]   # list of dicts: {"label": "LABEL_0", "score": 0.12}
        # Map indices to LABELS
        labeled = {LABELS[i]: s["score"] for i, s in enumerate(scores[:len(LABELS)])}
        # Pick top label and derive crude intensity
        top = max(labeled, key=labeled.get)
        intensity = round(labeled[top], 3)
        issues = []  # placeholder; later use rule-sets or a secondary small model
        return {"relationship_type": top, "intensity": intensity, "issues": issues}

_classifier = None
def get_classifier():
    global _classifier
    if _classifier is None:
        _classifier = RelationshipClassifier()
    return _classifier

def classify_relationship(messages: List[str]) -> Dict:
    return get_classifier().classify(messages)
