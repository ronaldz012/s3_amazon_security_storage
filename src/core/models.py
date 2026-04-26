import uuid
from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import ForeignKey, String, DateTime, Boolean, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class Book(Base):
    __tablename__ = "books"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    description: Mapped[str] = mapped_column(String, default="")

class User(Base):
    __tablename__ = "users"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    characters: Mapped[list["Character"]] = relationship(
        back_populates="owner",
        lazy="selectin"
    )

    
class Character(Base):
    __tablename__ = "characters"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(500), default="")
    
    # Metadata S3
    s3_key: Mapped[str] = mapped_column(String(512), nullable=False, unique=True)
    # Ejemplo: "users/abc-123/characters/mi-personaje.png"
    
    s3_bucket: Mapped[str] = mapped_column(String(255), nullable=False)
    original_filename: Mapped[str] = mapped_column(String(255), nullable=False)
    content_type: Mapped[str] = mapped_column(String(100), nullable=False)
    # Ejemplo: "image/png", "application/json"
    
    file_size_bytes: Mapped[int] = mapped_column(nullable=False)
    
    # Auditoría
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), 
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=True
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    
    # FK al usuario
    owner_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False)
    owner: Mapped["User"] = relationship(back_populates="characters")