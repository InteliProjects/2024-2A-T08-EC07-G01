from typing import Optional, List
from app.models.model import Model, ModelUpdate
from app.repositories.models_repo import ModelRepository


class ModelService:
    def __init__(self, model_repo: ModelRepository):
        self.model_repo = model_repo

    def get_all_models(self) -> List[Model]:
        return self.model_repo.get_all_models()

    def get_model(self, model_name: str) -> Optional[Model]:
        return self.model_repo.get_model(model_name)

    def create_model(self, model: Model) -> str:
        return self.model_repo.create_model(model)

    def update_model(self, model_name: str, model: ModelUpdate) -> bool:
        return self.model_repo.update_model(model_name, model)

    def delete_model(self, model_name: str) -> bool:
        return self.model_repo.delete_model(model_name)

    def get_models_by_type(self, model_type: str) -> List[Model]:
        return self.model_repo.get_models_by_type(model_type)

    def get_current_models(self) -> List[Model]:
        return self.model_repo.get_current_models()


class ModelServiceSingleton:
    _instance: Optional[ModelService] = None

    def __init__(self, *args, **kwargs):
        raise RuntimeError("Call get_instance() instead")

    def __new__(cls, *args, **kwargs):
        raise RuntimeError("Call get_instance() instead")

    @classmethod
    def initialize(cls, model_repo: ModelRepository):
        if cls._instance is None:
            cls._instance = ModelService(model_repo)

    @classmethod
    def get_instance(cls) -> ModelService:
        if cls._instance is None:
            raise Exception(
                "ModelServiceSingleton is not initialized. Call initialize() first."
            )

        return cls._instance
