from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security  import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user_schema import UserCreate, UserResponse, TokenResponse
from app.models.user_model import User
from app.db.database import get_session
from sqlalchemy.future import select
from app.core.security import get_password_hash, verify_password, create_access_token
from app.dependencies.auth import get_current_user


auth_router =APIRouter(tags=['Auth'])

@auth_router.post('/register', response_model=UserResponse)
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

@auth_router.post("/login", response_model=TokenResponse)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_session),
):
    result = await db.execute(select(User).filter(User.email == form_data.username))
    user = result.scalar()
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token({"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@auth_router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user