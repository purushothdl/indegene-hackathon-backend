from fastapi import Depends
from app.database.mongodb import mongodb
from app.repositories.file_repository import FileRepository
from app.services.file_service import FileService



# ----------------------------
# Repository Dependencies
# ----------------------------

def get_file_repository() -> FileRepository:
    """File repository dependency (MongoDB)"""
    return FileRepository(collection=mongodb.db.files)

# Add other repositories later (e.g., UserRepository, AuthRepository)



# ----------------------------
# Service Dependencies
# ----------------------------

def get_file_service(
    file_repository: FileRepository = Depends(get_file_repository)
) -> FileService:
    """File service dependency (business logic)"""
    return FileService(file_repository=file_repository)

# Add other services later (e.g., UserService, AuthService)