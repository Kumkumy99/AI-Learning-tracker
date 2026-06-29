from fastapi import APIRouter,Depends
from ..schemas.users import UserResponse
from ..security import get_current_user

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/me", response_model=UserResponse)
def get_me(current_user=Depends(get_current_user)):
    return current_user