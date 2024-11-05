from gridfs import GridFS, GridOut
from typing import BinaryIO
from bson import ObjectId


class GridFSService:
    def __init__(self, gridfs: GridFS):
        self.fs = gridfs

    def upload_file(self, filename: str, file_data: BinaryIO) -> str:
        file_id = self.fs.put(file_data, filename=filename)
        return str(file_id)

    def download_file(self, file_id: str) -> GridOut:
        return self.fs.get(ObjectId(file_id))

    def delete_file(self, file_id: str) -> bool:
        self.fs.delete(ObjectId(file_id))
        return True
