from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.responses_model import Response as ResponseModel
from app.models.user_model import User
from app.models.vacancy_model import Vacancy
from app.schemas.response_schema import ResponseCreate, ResponseOut, ResponseUpdate, ResponseStatus
from app.db.database import get_session
from app.dependencies.auth import get_current_user

response_router = APIRouter(tags=["Responses"], prefix='/responses')

@response_router.post('/add', response_model=ResponseOut)
async def add_response(
    resp: ResponseCreate, 
    db: AsyncSession=Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    result_vacancy = await db.execute(select(Vacancy).filter(Vacancy.id == resp.vacancy_id))
    vacancy = result_vacancy.scalar_one_or_none()

    if vacancy is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Vacancy not found')

    response_user = await db.execute(
        select(ResponseModel).filter(
            ResponseModel.user_id == current_user.id, 
            ResponseModel.vacancy_id == resp.vacancy_id))
    user = response_user.scalar_one_or_none()

    if user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='such a response already exists')

    new_response = ResponseModel(
        user_id = current_user.id,
        vacancy_id = vacancy.id,
        text= resp.text,
    )

    db.add(new_response)

    await db.commit()
    await db.refresh(new_response)

    return new_response

@response_router.get('/my')
async def my_responses(db: AsyncSession= Depends(get_session), current_user: User = Depends(get_current_user)):
    results = await db.execute(select(ResponseModel).filter(ResponseModel.user_id == current_user.id))
    my_responses = results.scalars().all()

    return my_responses

@response_router.get('/{vanacy_id}')
async def vacancy_response(vanacy_id: int, 
                           db: AsyncSession= Depends(get_session), 
                           current_user: User = Depends(get_current_user)):
    result_vacany = await db.execute(select(Vacancy).filter(Vacancy.id == vanacy_id))
    vacancy = result_vacany.scalar_one_or_none()

    if vacancy is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Vacancy not found')
    
    if vacancy.author_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail ='You dont have access to this vacancy responses')

    result_response = await db.execute(select(ResponseModel).filter(ResponseModel.vacancy_id == vanacy_id))
    respon = result_response.scalars().all()

    return respon

@response_router.patch("/{response_id}/update")
async def update_response(response_id: int,
                          resup: ResponseUpdate, 
                           db: AsyncSession= Depends(get_session), 
                           current_user: User = Depends(get_current_user)):
    result_resp = await db.execute(select(ResponseModel).filter(ResponseModel.id == response_id))
    response = result_resp.scalar_one_or_none()

    if response is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Responses not found')
    
    vacancy_user = await db.execute(select(Vacancy).filter(Vacancy.id == response.vacancy_id))
    vacancy = vacancy_user.scalar_one_or_none()

    if vacancy.author_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You dont have access to this vacancy responses')
    
    response.status = resup.status

    await db.commit()
    await db.refresh(response)

    return response

@response_router.delete("/{response_id}/delete")
async def delete_response(
    response_id: int,
    db: AsyncSession= Depends(get_session), 
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(select(ResponseModel).filter(ResponseModel.id == response_id))
    response = result.scalar_one_or_none()

    if response is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Responses not found')
    
    if response.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You dont have access to this vacancy responses')

    db.delete(response)

    await db.commit()
    return {'message': 'Delete is successful'} 