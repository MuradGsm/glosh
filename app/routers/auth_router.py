from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user_schema import UserCreate, UserResponse
from app.models.user_model import User
from app.db.database import get_session
from sqlalchemy.future import select
from app.core.security import get_password_hash

router =APIRouter()

@router.post('/register', response_model=UserResponse)
async def register(user:UserCreate, db: AsyncSession=Depends(get_session)):
    existing_user = await db.execute(select(User).filter(User.email == user.email))
    existing_user = existing_user.scalar()

    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User email is already')
    
    hashed_password=get_password_hash(user.password)

    new_user = User(
        phone_number=user.phone_number,
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        hashed_password=hashed_password,
        is_employer=user.is_employer,
        is_employee=user.is_employee
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user