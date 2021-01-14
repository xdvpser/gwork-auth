from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud, schemes
from app.api import deps

router = APIRouter()


@router.post("/registration", status_code=status.HTTP_201_CREATED)
def register_user(user_in: schemes.UserRegister, db: Session = Depends(deps.get_db)):
    user = crud.user.get_by_username(db, username=user_in.username)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    crud.user.register(db, obj_in=user_in)


@router.post("/login")
def login(user_in: schemes.UserLogin, db: Session = Depends(deps.get_db)):
    pass
