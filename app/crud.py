# app/crud.py
from sqlmodel import Session, select
from .models import MediaFile
from typing import List

def create_media_file(session: Session, media: MediaFile):
    session.add(media)
    session.commit()
    session.refresh(media)
    return media

def get_media_files(session: Session, skip: int = 0, limit: int = 100) -> List[MediaFile]:
    statement = select(MediaFile).offset(skip).limit(limit)
    results = session.exec(statement)
    return results.all()
