from typing import List, Optional, Dict
from bson import ObjectId
from pymongo.collection import Collection

from app.utils.mongo_utils import convert_objectids_to_strings

class FileRepository:
    def __init__(self, collection: Collection):
        self.collection = collection  

    async def create_file(self, file_data: Dict) -> Dict:
        result = await self.collection.insert_one(file_data)
        return await self.get_file_by_id(result.inserted_id)

    async def get_file_by_id(self, file_id: str) -> Optional[Dict]:
        file = await self.collection.find_one({"_id": ObjectId(file_id)})
        return convert_objectids_to_strings(file) if file else None

    async def get_file_by_name(self, file_name: str) -> Optional[Dict]:
        file = await self.collection.find_one({"file_name": file_name})
        return convert_objectids_to_strings(file) if file else None

    async def update_file(self, file_id: str, update_data: Dict) -> bool:
        result = await self.collection.update_one(
            {"_id": ObjectId(file_id)}, {"$set": update_data}
        )
        return result.modified_count > 0

    async def delete_file(self, file_id: str) -> bool:
        result = await self.collection.delete_one({"_id": ObjectId(file_id)})
        return result.deleted_count > 0

    async def search_files_by_name(self, search_string: str) -> List[Dict]:
        # Case-insensitive search for files containing the search string
        files = await self.collection.find(
            {"file_name": {"$regex": search_string, "$options": "i"}}
        ).to_list(None)
        for file in files:
            convert_objectids_to_strings(file)
        return files