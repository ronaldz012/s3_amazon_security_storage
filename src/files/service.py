import uuid
import boto3
from botocore.exceptions import ClientError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from core.models import Character
from core.exceptions import AppException, InternalException
from core.s3_client import get_s3_client
from config import settings
ALLOWED_CONTENT_TYPES = {"image/png", "image/jpeg", "image/webp", "application/pdf"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
class FileService:
    def __init__(self, session: AsyncSession):
        self.s3 = get_s3_client()
        self.bucket = settings.S3_BUCKET_NAME
        self.session = session

    def _build_key(self, owner_id: str, filename: str) -> str:
        ext = filename.rsplit(".", 1)[-1] if "." in filename else ""
        unique = uuid.uuid4().hex
        return f"users/{owner_id}/characters/{unique}.{ext}"

    def _generate_presigned_url(self, s3_key: str, expires: int = 3600) -> str:
        try:
            return self.s3.generate_presigned_url(
                "get_object",
                Params={"Bucket": self.bucket, "Key": s3_key},
                ExpiresIn=expires,
            )
        except ClientError:
            raise InternalException("No se pudo generar la URL del archivo")

    async def upload_file(
        self,
        owner_id: str,
        file_bytes: bytes,
        original_filename: str,
        content_type: str,
    ) -> Character:
        
        if content_type not in ALLOWED_CONTENT_TYPES:
            raise AppException("Tipo de archivo no permitido", status_code=415)
    
        if len(file_bytes) > MAX_FILE_SIZE:
            raise AppException("Archivo demasiado grande", status_code=413)
        s3_key = self._build_key(owner_id, original_filename)

        try:
            self.s3.put_object(
                Bucket=self.bucket,
                Key=s3_key,
                Body=file_bytes,
                ContentType=content_type,
            )
        except ClientError:
            raise InternalException("Error al subir el archivo a S3")

        character = Character(
            name=original_filename,
            original_filename=original_filename,
            content_type=content_type,
            file_size_bytes=len(file_bytes),
            s3_key=s3_key,
            s3_bucket=self.bucket,
            owner_id=owner_id,
        )
        self.session.add(character)
        await self.session.commit()
        await self.session.refresh(character)
        return character

    async def get_files_by_user(self, owner_id: str) -> list[dict]:
        stmt = (
            select(Character)
            .where(Character.owner_id == owner_id, Character.is_active == True)
            .order_by(Character.created_at.desc())
        )
        result = await self.session.execute(stmt)
        characters = result.scalars().all()

        return [
            {**c.__dict__, "url": self._generate_presigned_url(c.s3_key)}
            for c in characters
        ]