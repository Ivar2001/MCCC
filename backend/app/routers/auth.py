from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from secrets import token_urlsafe
from datetime import timedelta, datetime

from ..database import get_db
from ..models import User, RegistrationCode
from ..schemas import UserCreate, UserResponse, Token, LoginRequest
from ..auth import (
    get_password_hash, 
    verify_password, 
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    get_current_user
)

router = APIRouter(prefix="/api/auth", tags=["authentication"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user with a valid registration code"""
    
    # Check if registration code is valid
    reg_code = db.query(RegistrationCode).filter(
        RegistrationCode.code == user_data.registration_code
    ).first()
    
    if not reg_code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid registration code"
        )
    
    # Check if code is already fully used
    if reg_code.max_uses > 0 and reg_code.current_uses >= reg_code.max_uses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Registration code has already been used"
        )
    
    # Check if username already exists
    existing_user = db.query(User).filter(User.username == user_data.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    # Check if email already exists
    existing_email = db.query(User).filter(User.email == user_data.email).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user with hashed password
    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_password,
        registration_code_used=user_data.registration_code
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Update registration code usage
    reg_code.current_uses += 1
    if reg_code.max_uses == 1:  # Single-use code
        reg_code.is_used = True
        reg_code.used_by_user_id = new_user.id
        reg_code.used_at = datetime.utcnow()
    
    db.commit()
    
    return new_user

@router.post("/login", response_model=Token)
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    """Login and get access token"""
    
    # Find user by username
    user = db.query(User).filter(User.username == login_data.username).first()
    
    # Verify user exists and password is correct
    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/admin/generate-code")
def generate_registration_code(
    max_uses: int = 1,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Generate a new registration code (admin only - you can add proper admin check later)"""
    
    # Generate random code
    code = token_urlsafe(16)  # Generates something like: "K7jN9mP2qR4sT6vX8yZ"
    
    new_code = RegistrationCode(
        code=code,
        max_uses=max_uses
    )
    
    db.add(new_code)
    db.commit()
    db.refresh(new_code)
    
    return {
        "code": new_code.code,
        "max_uses": new_code.max_uses,
        "message": f"Registration code generated. Share this code: {new_code.code}"
    }

@router.get("/me", response_model=UserResponse)
def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current logged-in user info"""
    return current_user