from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
import os
import shutil
from datetime import datetime

from ..database import get_db
from ..models import User, Can
from ..schemas import CanCreate, CanResponse, CanUpdate
from ..auth import get_current_user

router = APIRouter(prefix="/api/cans", tags=["cans"])

# Directory for uploaded images
UPLOAD_DIR = "/app/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.get("/", response_model=List[CanResponse])
def get_all_cans(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all cans for the current user"""
    cans = db.query(Can).filter(Can.user_id == current_user.id).all()
    return cans

@router.post("/", response_model=CanResponse, status_code=status.HTTP_201_CREATED)
def create_can(
    can_data: CanCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new can in the collection"""
    new_can = Can(
        flavor=can_data.flavor,
        type=can_data.type,
        year=can_data.year,
        origin=can_data.origin,
        condition=can_data.condition,
        description=can_data.description,
        user_id=current_user.id
    )
    
    db.add(new_can)
    db.commit()
    db.refresh(new_can)
    
    return new_can

@router.get("/{can_id}", response_model=CanResponse)
def get_can(
    can_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific can by ID"""
    can = db.query(Can).filter(
        Can.id == can_id,
        Can.user_id == current_user.id
    ).first()
    
    if not can:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Can not found"
        )
    
    return can

@router.put("/{can_id}", response_model=CanResponse)
def update_can(
    can_id: int,
    can_data: CanUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a can"""
    can = db.query(Can).filter(
        Can.id == can_id,
        Can.user_id == current_user.id
    ).first()
    
    if not can:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Can not found"
        )
    
    # Update fields if provided
    if can_data.flavor not in (None, "", "string"):
        can.flavor = can_data.flavor
    if can_data.type not in (None, "", "string"):
        can.type = can_data.type
    if can_data.year != None and can_data.year != 0:
        can.year = can_data.year
    if can_data.origin not in (None, "", "string"):
        can.origin = can_data.origin
    if can_data.condition not in (None, "", "string"):
        can.condition = can_data.condition
    if can_data.description not in (None, "", "string"):
        can.description = can_data.description
    
    db.commit()
    db.refresh(can)
    
    return can

@router.delete("/{can_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_can(
    can_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a can"""
    can = db.query(Can).filter(
        Can.id == can_id,
        Can.user_id == current_user.id
    ).first()
    
    if not can:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Can not found"
        )
    
    # Delete associated image if exists
    if can.image_path and os.path.exists(can.image_path):
        os.remove(can.image_path)
    
    db.delete(can)
    db.commit()
    
    return None

@router.post("/{can_id}/upload-image", response_model=CanResponse)
async def upload_can_image(
    can_id: int,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Upload an image for a can"""
    can = db.query(Can).filter(
        Can.id == can_id,
        Can.user_id == current_user.id
    ).first()
    
    if not can:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Can not found"
        )
    
    # Validate file type
    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be an image"
        )
    
    # Generate unique filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_extension = os.path.splitext(file.filename)[1]
    filename = f"can_{can_id}_{timestamp}{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, filename)
    
    # Save file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Delete old image if exists
    if can.image_path and os.path.exists(can.image_path):
        os.remove(can.image_path)
    
    # Update database
    can.image_path = file_path
    db.commit()
    db.refresh(can)
    
    return can