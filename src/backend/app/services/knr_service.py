from typing import Optional

from app.repositories.knr_repo import KNRRepository
from app.models.knr import KNR, KNRUpdate


class KNRService:
    def __init__(self, knr_repo: KNRRepository):
        self.knr_repo = knr_repo

    def get_all_knrs(self) -> list[KNR]:
        return self.knr_repo.get_all_knrs()

    def create_knr(self, knr: KNR) -> str:
        return self.knr_repo.create_knr(knr)

    def get_knr(self, knr_id: str) -> Optional[KNR]:
        return self.knr_repo.get_knr(knr_id)

    def update_knr(self, knr_id: str, knr: KNRUpdate | KNR) -> bool:
        return self.knr_repo.update_knr(knr_id, knr)

    def delete_knr(self, knr_id: str) -> bool:
        return self.knr_repo.delete_knr(knr_id)


class KNRServiceSingleton:
    __instance: Optional[KNRService] = None

    def __init__(self, *args, **kwargs):
        raise RuntimeError("Call get_instance() instead")

    def __new__(cls, *args, **kwargs):
        raise RuntimeError("Call get_instance() instead")

    @staticmethod
    def initialize(knr_repo: KNRRepository):
        KNRServiceSingleton.__instance = KNRService(knr_repo)

    @staticmethod
    def get_instance() -> KNRService:
        if KNRServiceSingleton.__instance is None:
            raise RuntimeError("KNRServiceSingleton not initiated yet")

        return KNRServiceSingleton.__instance
