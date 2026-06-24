from fastapi import APIRouter,Depends,HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from .. models import User
from ..schemas import UserCreate,UserResponse,UserLogin,Token
from .. auth import hash_password,verify_password,create_access_token,get_current_user
router = APIRouter(
    prefix="/users",
    tags=["Users"]
)
@router.post("/", response_model=UserResponse)
def create_user(user:UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_pw = hash_password(user.password)
    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_pw
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# app/routers/users.py

@router.post("/login", response_model=Token)
@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
     db_user = db.query(User).filter(
    User.email == form_data.username
).first()

     if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

     if not verify_password( form_data.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect password")
     token_data = {
    "sub": db_user.email
}
     access_token = create_access_token(data=token_data)
     return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.get("/me")
def read_me(current_user: User = Depends(get_current_user)):
    return current_user