# app/routers/media.py
from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from sqlmodel import Session
from typing import List
import os
from uuid import uuid4
from .. import models, schemas, crud
from ..database import get_session
from app import settings
import shutil
from fastapi.responses import StreamingResponse
import requests

router = APIRouter()

@router.post("/uploadfile/", response_model=schemas.MediaFileRead)
async def create_upload_file(
    media_type: str,
    file: UploadFile = File(...),
    session: Session = Depends(get_session)
):
    # Validate media_type
    if media_type not in ["image", "video"]:
        raise HTTPException(status_code=400, detail="Invalid media_type. Must be 'image' or 'video'.")

    # Validate file content type based on media_type
    if media_type == "image" and not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Uploaded file is not an image.")
    if media_type == "video" and not file.content_type.startswith("video/"):
        raise HTTPException(status_code=400, detail="Uploaded file is not a video.")

    # Generate a unique filename to prevent collisions
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid4().hex}{file_extension}"
    file_path = os.path.join("media", unique_filename)

    # Ensure the 'media' directory exists
    os.makedirs("media", exist_ok=True)

    # Save the uploaded file to the media directory
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {e}")
    finally:
        file.file.close()

    # Construct the CDN URL for the uploaded file
    url = f"{settings.CDN_URL}{unique_filename}"

    # Create a new MediaFile record in the database
    media = models.MediaFile(
        filename=unique_filename,
        media_type=media_type,
        url=url
    )
    crud.create_media_file(session, media)

    return media

@router.get("/", response_model=List[schemas.MediaFileRead])
def read_media_files(skip: int = 0, limit: int = 100, session: Session = Depends(get_session)):
    media_files = crud.get_media_files(session, skip=skip, limit=limit)
    return media_files


@router.get("/preview/")
def preview_video(url: str):
    # Check if the URL is valid
    if not url.startswith("http"):
        raise HTTPException(status_code=400, detail="Invalid URL")

    try:
        # Stream the video from the provided URL
        response = requests.get(url, stream=True, verify=False)  # Disable SSL verification for testing
        response.raise_for_status()  # Check if the request was successful

        # Return a StreamingResponse for the video content
        return StreamingResponse(response.iter_content(chunk_size=1024), media_type="video/mp4")

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve video: {e}")