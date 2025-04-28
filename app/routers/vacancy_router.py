from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.schemas.vacancy_schema import VacancyResponse, VacancyCreate
from app.db.database import get_session
from app.models.user_model import User
from app.dependencies.auth import get_current_user
from app.models.vacancy_model import Vacancy

vacancy_router = APIRouter()

@vacancy_router.post('/vacancy/add', response_model=VacancyResponse)
async def add_vacany(
    vacancy: VacancyCreate, 
    db: AsyncSession= Depends(get_session), 
    current_user: User = Depends(get_current_user)
) -> dict:
    new_vacancy = Vacancy(
        title= vacancy.title,
        description=vacancy.description,
        salary_from=vacancy.salary_from,
        salary_to=vacancy.salary_to,
        author_id=current_user.id
    )

    db.add(new_vacancy)
    await db.commit()
    await db.refresh(new_vacancy)

    return new_vacancy

@vacancy_router.get('/vacany/all')
async def get_all_vacancies(db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(Vacancy).limit(10).offset(0))
    vacancies = result.scalars().all()

    return vacancies

@vacancy_router.get('/vacancy/{vacancy_id}', response_model=VacancyResponse)
async def get_vacancy(vacancy_id: int, db: AsyncSession=Depends(get_session)):
    result = await db.execute(select(Vacancy).filter(Vacancy.id == vacancy_id))
    vacancy = result.scalar_one_or_none()

    if vacancy is None:
        raise  HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Vacancy not found')
    
    return vacancy

@vacancy_router.delete('/vacancy/delete/{vacany_id}')
async def delete_vacancy(vacancy_id: int, db: AsyncSession = Depends(get_session), current_user: User = Depends(get_current_user)):
    result = await db.execute(select(Vacancy).filter(Vacancy.id == vacancy_id))
    vacancy = result.scalar_one_or_none()

    if vacancy is None:
        raise  HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Vacancy not found')
    
    if vacancy.author_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You can not delete this object')
    
    db.delete(vacancy)

    await db.commit()

    return {'message': 'Delete is successful'}
