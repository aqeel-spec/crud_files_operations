# app/schemas.py
from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel

class MediaFileBase(SQLModel):
    filename: str
    media_type: str
    url: str

class MediaFileCreate(MediaFileBase):
    pass

class MediaFileRead(MediaFileBase):
    id: int
    uploaded_at: datetime

    class Config:
        orm_mode = True
