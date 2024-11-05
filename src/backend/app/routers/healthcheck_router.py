from fastapi import APIRouter, HTTPException
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure


mongo_url = "mongodb://localhost:27017"
router = APIRouter(prefix="/healthcheck/mongodb", tags=["healthcheck_mongodb"])


@router.get("/")
async def healthcheck_mongodb():
    try:
        client = MongoClient(mongo_url, serverSelectionTimeoutMS=1000)
        client.server_info()
        return {"status": "MongoDB reachable", "status_code": 200}
    except:
        #raise HTTPException(status_code=500, detail="MongoDB not reachable")
        return {"status": "MongoDB not reachable", "status_code": "Error"}



