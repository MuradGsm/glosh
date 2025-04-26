from fastapi import Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordBearer
from app.db.database import get_session
from app.core.config import settings
from jose import JWTError, jwt
from sqlalchemy.future import select
from app.models.user_model import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/login')

async def get_current_user(
        token: str=Depends(oauth2_scheme),
        db: AsyncSession=Depends(get_session)
):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

        user_email: str = payload.get('sub')
        if user_email is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Token does not contain email")
        
        result = await db.execute(select(User).filter(User.email == user_email))
        user = result.scalar()

        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
        return user
    
    except JWTError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid token or expired: {str(e)}")
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal error: {str(e)}"
        )