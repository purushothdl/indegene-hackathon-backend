
### File Exceptions
class FileUploadError(Exception):
    """Raised when file upload fails."""
    pass

class FileNotFoundError(Exception):
    """Raised when a file is not found in the database."""
    pass

