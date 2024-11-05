from app.models.predictions import Prediction


def mock_prediction() -> Prediction:
    return Prediction(
        KNR="top10knrsdavolkswagen",
        predicted_fail_codes=[1, 2, 3],
        real_fail_codes=[1, 2, 3],
        indicated_tests=["test1", "test2", "test3"],
    )
