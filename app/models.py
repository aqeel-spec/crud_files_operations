# app/models.py
from sqlmodel import SQLModel, Field 
from typing import Optional
from datetime import datetime

class MediaFile(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    filename: str
    media_type: str  # 'image' or 'video'
    url: str
    uploaded_at: datetime = Field(default_factory=datetime.utcnow)
