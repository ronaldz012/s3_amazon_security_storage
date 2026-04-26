from jose import JWTError, jwt
from fastapi import HTTPException, status
from config import settings

class CurrentUserService:
    def __init__(self, token: str):
        self.token = token

    def get_user_id(self) -> str:
        try:
            payload = jwt.decode(self.token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            user_id: str | None = payload.get("sub")
            if user_id is None:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
            return user_id
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)