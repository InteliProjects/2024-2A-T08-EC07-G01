from app.models.model import Model
from app.models.metrics import MetricsWeights

def calculate_weight(metrics_weights: MetricsWeights, model: Model) -> dict:
    result = {
        "accuracy": metrics_weights.accuracy * model.accuracy if metrics_weights.accuracy is not None else None,
        "precision": metrics_weights.precision * model.precision if metrics_weights.precision is not None else None,
        "recall": metrics_weights.recall * model.recall if metrics_weights.recall is not None else None,
        "f1_score": metrics_weights.f1_score * model.f1_score if metrics_weights.f1_score is not None else None
    }
    return result
    