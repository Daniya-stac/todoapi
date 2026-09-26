from typing import Annotated
from fastapi import HTTPException, status, APIRouter, Query
from sqlmodel import select
from backend.database.conf import SessionDep
from backend.database.models import ItemBase, Item, ItemUpdate

router = APIRouter(prefix='/todos',
                   tags=['todos'])


@router.get('/', response_model=list[Item])
def all_tasks(session: SessionDep,
              offset: int = 0,
              limit: Annotated[int, Query(le=100)] = 100, ):
    tasks = session.exec(select(Item).offset(offset).limit(limit)).all()
    return tasks


@router.get('/{id}/', response_model=Item)
def specific_task(id: int, session: SessionDep):
    task = session.get(Item, id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Задача не была найдена'
        )
    return task


@router.post('/', response_model=Item, status_code=status.HTTP_201_CREATED)
def create_task(item: ItemBase, session: SessionDep):
    db_task = Item.model_validate(item)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task


@router.patch('/{id}/', response_model=Item)
def change_task(id: int, item: ItemUpdate, session: SessionDep):
    task_db = session.get(Item, id)
    if not task_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Задача не была найдена'
        )
    task_data = item.model_dump(exclude_unset=True)
    task_db.sqlmodel_update(task_data)
    session.add(task_db)
    session.commit()
    session.refresh(task_db)
    return task_db


@router.delete('/{id}/', status_code=status.HTTP_204_NO_CONTENT)
def delete_task(id: int, session: SessionDep):
    task = session.get(Item, id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Задача не была найдена'
        )
    session.delete(task)
    session.commit()
    return
