from typing import Dict, List
from fastapi import UploadFile
from app.repositories.file_repository import FileRepository
from app.core.google_cloud_storage import gcs
from app.core.exceptions import FileUploadError
import uuid

class FileService:
    def __init__(self, file_repository: FileRepository):
        self.file_repository = file_repository  

    async def upload_file(
        self,
        file: UploadFile,
        file_name: str,
        description: str = None
    ) -> dict:
        try:
            # Upload to GCS
            file_extension = file.filename.split(".")[-1]
            gcs_path = f"indegene_hack/files/{uuid.uuid4()}.{file_extension}"
            file_url = await gcs.upload_file(file, gcs_path)
            
            # Create metadata
            file_data = {
                "file_name": file_name,
                "description": description,
                "url": file_url,
                "mime_type": file.content_type
            }
            return await self.file_repository.create_file(file_data)
            
        except Exception as e:
            raise FileUploadError(f"Upload failed: {str(e)}")
        
    async def get_file_by_id(self, file_id: str) -> Dict:
        file = await self.file_repository.get_file_by_id(file_id)
        if not file:
            raise FileNotFoundError("File not found")
        return file

    async def get_file_by_name(self, file_name: str) -> Dict:
        file = await self.file_repository.get_file_by_name(file_name)
        if not file:
            raise FileNotFoundError("File not found")
        return file

    async def update_file(self, file_id: str, update_data: Dict) -> bool:
        updated = await self.file_repository.update_file(file_id, update_data)
        if not updated:
            raise FileNotFoundError("File not found or no changes made")
        return True

    async def delete_file(self, file_id: str) -> bool:
        deleted = await self.file_repository.delete_file(file_id)
        if not deleted:
            raise FileNotFoundError("File not found")
        return True

    async def search_files_by_name(self, search_string: str) -> List[Dict]:
        files = await self.file_repository.search_files_by_name(search_string)
        if not files:
            raise FileNotFoundError("No files found matching the search")
        return files