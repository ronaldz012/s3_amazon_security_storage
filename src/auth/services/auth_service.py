from datetime import datetime, timedelta, timezone
from typing import Optional

# CORRECCIÓN: Imports correctos de SQLAlchemy
import bcrypt
from sqlalchemy import select, or_ 
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from jose import jwt
from passlib.context import CryptContext

from config import settings
from core.models import User
from ..schemas import LoginDTO, LoginSuccessDTO, RegisterDTO, UserResponseDTO
from core.exceptions import AppException, NotFoundException



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    def __init__(self, session: AsyncSession):
        self.session = session

    
    def _hash_password(self, password: str) -> str:
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    def _verify_password(self, plain: str, hashed: str) -> bool:
        return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))

    def _create_access_token(self, user_id: str) -> str:
        now = datetime.now(timezone.utc)
        expire = now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        payload = {"sub": str(user_id), "iat": now, "exp": expire}
        return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    



    async def _get_user_by_username(self, username_dto: str) -> Optional[User]:
        # CORRECCIÓN: Usar select() en lugar de Select()
        statement = select(User).where(User.username == username_dto)
        result = await self.session.execute(statement)
        return result.scalars().first()




    async def login(self, dto: LoginDTO) -> LoginSuccessDTO:
        user = await self._get_user_by_username(dto.username)

        if not user or not self._verify_password(dto.password, user.hashed_password):
            # Seguridad: No digas si falló el usuario o la contraseña específicamente
            raise AppException("Invalid credentials")

        if not user.is_active:
            raise AppException("User inactive")

        token = self._create_access_token(user.id)
        return LoginSuccessDTO(
            access_token=token,
            user=UserResponseDTO.model_validate(user)
        )




    async def register(self, dto: RegisterDTO) -> LoginSuccessDTO:
        stmt = select(User).where(
            or_(User.username == dto.username, User.email == dto.email)
        )
        
        check_user = await self.session.execute(stmt)
        if check_user.scalars().first():
            raise AppException("Username or email already exists")

        new_user = User(
            username=dto.username,
            email=dto.email,
            hashed_password=self._hash_password(dto.password)
        )

        try:
            self.session.add(new_user)
            await self.session.commit()
            await self.session.refresh(new_user)
        except IntegrityError:
            await self.session.rollback()
            raise AppException("Conflict creating user: duplicate data")

        token = self._create_access_token(new_user.id)
        return LoginSuccessDTO(
            access_token=token,
            user=UserResponseDTO.model_validate(new_user)
        )