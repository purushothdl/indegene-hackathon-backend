from fastapi import APIRouter, UploadFile, Form, Depends, Query
from app.services.file_service import FileService
from app.dependencies.dependencies import get_file_service

file_router = APIRouter(prefix="/files")

# Upload File
@file_router.post("/upload", status_code=201)
async def upload_file(
    file: UploadFile,
    file_name: str = Form(...),
    description: str = Form(None),
    file_service: FileService = Depends(get_file_service)
):
    return await file_service.upload_file(file, file_name, description)

# Search Files by Name
@file_router.get("/search")
async def search_files_by_name(
    query: str = Query(..., description="Search string for file names"),
    file_service: FileService = Depends(get_file_service)
):
    return await file_service.search_files_by_name(query)

# Get File by ID
@file_router.get("/{file_id}")
async def get_file_by_id(
    file_id: str,
    file_service: FileService = Depends(get_file_service)
):
    return await file_service.get_file_by_id(file_id)

# Get File by Name
@file_router.get("/name/{file_name}")
async def get_file_by_name(
    file_name: str,
    file_service: FileService = Depends(get_file_service)
):
    return await file_service.get_file_by_name(file_name)

# Update File
@file_router.put("/{file_id}")
async def update_file(
    file_id: str,
    file_name: str = Form(None),
    description: str = Form(None),
    file_service: FileService = Depends(get_file_service)
):
    update_data = {}
    if file_name:
        update_data["file_name"] = file_name
    if description:
        update_data["description"] = description
    return await file_service.update_file(file_id, update_data)

# Delete File
@file_router.delete("/{file_id}")
async def delete_file(
    file_id: str,
    file_service: FileService = Depends(get_file_service)
):
    return await file_service.delete_file(file_id)