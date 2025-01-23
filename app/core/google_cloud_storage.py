from google.cloud import storage
from app.core.config import settings
import os

class GoogleCloudStorage:
    def __init__(self):
        self.client = storage.Client.from_service_account_json(
            settings.GCP_CREDENTIALS_PATH
        )
        self.bucket = self.client.bucket(settings.GCS_BUCKET)

    async def upload_file(self, file, destination_name: str) -> str:
        blob = self.bucket.blob(destination_name)
        blob.upload_from_file(file.file)
        return blob.public_url

gcs = GoogleCloudStorage()