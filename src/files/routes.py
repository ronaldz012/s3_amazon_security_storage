from typing import Annotated
from fastapi import APIRouter, Depends, UploadFile, File
from auth.dependencies import CurrentUserServiceDep
from files.dependencies import FileServiceDep
from files.schemas import FileListDTO, FileUploadResponseDTO

from typing import List

file_router = APIRouter(prefix="/files", tags=["Files"])


@file_router.post("/upload", response_model=FileUploadResponseDTO, status_code=201)
async def upload_file(
    current_user:CurrentUserServiceDep,
    service: FileServiceDep,
    file: UploadFile = File(...),
):
    file_bytes = await file.read()
    return await service.upload_file(
        owner_id=current_user.get_user_id(),
        file_bytes=file_bytes,
        original_filename=file.filename or "unknown",
        content_type=file.content_type or "application/octet-stream",
    )


@file_router.get("/", response_model=List[FileListDTO])
async def get_my_files(
    current_user: CurrentUserServiceDep,
    service: FileServiceDep,
):
    return await service.get_files_by_user(owner_id=current_user.get_user_id())