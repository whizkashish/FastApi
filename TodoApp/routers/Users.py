from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status, Path
from models import Users
from database import SessionLocal
from .auth import get_current_user, bcrypt_context

router = APIRouter(
    prefix='/user',
    tags=['user']
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_depenency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


class UpdatePhoneNumberRequest(BaseModel):
    phone_number: str


class ChangePasswordRequest(BaseModel):
    password: str
    new_password: str


@router.get("/", status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency, db: db_depenency):
    if user is None:
        raise HTTPException(status=401, detail='Authentication Failed')
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()

    if user_model is None:
        raise HTTPException(status=401, detail='Authentication Failed')

    return user_model


@router.put("/change-password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user: user_dependency, db: db_depenency, form_request: ChangePasswordRequest):
    if user is None:
        raise HTTPException(status=401, detail='Authentication Failed')

    user_model = db.query(Users).filter(Users.id == user.get('id')).first()

    if user_model is None:
        raise HTTPException(status_code=404, detail='User not found!')

    if not bcrypt_context.verify(form_request.password, user_model.hashed_password):
        raise HTTPException(status_code=401, detail='Error on password change')

    user_model.hashed_password = bcrypt_context.hash(form_request.new_password)
    db.add(user_model)
    db.commit()


@router.put("/update-phone-number", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user: user_dependency, db: db_depenency, form_request: UpdatePhoneNumberRequest):
    if user is None:
        raise HTTPException(status=401, detail='Authentication Failed')

    user_model = db.query(Users).filter(Users.id == user.get('id')).first()

    if user_model is None:
        raise HTTPException(status_code=404, detail='User not found!')
    user_model.phone_number = form_request.phone_number
    db.add(user_model)
    db.commit()
