from datetime import datetime
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Mapped

class FileUploadResponseDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    original_filename: str
    content_type: str
    file_size_bytes: int
    s3_key: str
    created_at: datetime

class FileListDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    original_filename: str
    content_type: str
    file_size_bytes: int
    created_at: datetime
    url: str  # presigned URL generada en el servicio