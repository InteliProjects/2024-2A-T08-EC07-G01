from datetime import datetime
from typing import Optional

from app.db.mongodb import MongoDB
from app.models.knr import KNR, KNRUpdate


class KNRRepository:
    def __init__(self, db: MongoDB):
        self.db = db
        self.collection = db.get_collection("knrs")

    def get_all_knrs(self) -> list[KNR]:
        documents = self.collection.find()
        return [KNR(**document) for document in documents]

    def create_knr(self, knr: KNR) -> str:
        self.collection.insert_one(knr.model_dump(by_alias=True))
        return str(knr.KNR)

    def get_knr(self, knr_id: str) -> Optional[KNR]:
        document = self.collection.find_one({"KNR": knr_id})
        return KNR(**document) if document else None

    def update_knr(self, knr_id: str, knr: KNRUpdate | KNR) -> bool:
        result = self.collection.update_one(
            {"KNR": knr_id},
            {"$set": knr.model_dump(exclude_unset=True, by_alias=True)},
        )
        return result.modified_count > 0

    def delete_knr(self, knr_id: str) -> bool:
        result = self.collection.delete_one({"KNR": knr_id})
        return result.deleted_count > 0

    def get_knr_by_month(self, month: int, year: int):
        start_date = datetime(year, month, 1)
        if month == 12:
            end_date = datetime(year + 1, 1, 1)
        else:
            end_date = datetime(year, month + 1, 1)

        knr_documents = self.collection.find(
            {"DATA": {"$gte": start_date, "$lt": end_date}}, {"KNR": 1, "_id": 0}
        )

        return [doc["KNR"] for doc in knr_documents]
