from fastapi import HTTPException, status, APIRouter
from backend.schemas.schem import ItemsCreate, ItemsUpdate, ItemsResponse

fake_data: dict[int, dict] = {}
task_id = 1

router = APIRouter(prefix='/todos',
                   tags=['todos'])


@router.get('/', response_model=list[ItemsResponse])
def all_todos():
    return list(fake_data.values())


@router.get('/{id}/', response_model=ItemsResponse)
def specific_todo(id: int):
    if id in fake_data:
        return fake_data[id]
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='Задача не была найдена'
    )


@router.post('/', response_model=ItemsResponse, status_code=status.HTTP_201_CREATED)
def add_task(item: ItemsCreate):
    global task_id
    task = item.model_dump()
    task['id'] = task_id
    fake_data[task_id] = task
    task_id += 1
    return task


@router.patch('/{id}/', response_model=ItemsResponse)
def change_task(id: int, item: ItemsUpdate):
    if id in fake_data:
        update_task = item.model_dump(exclude_unset=True)
        fake_data[id].update(update_task)
        return fake_data[id]
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='Задача не была найдена'
    )


@router.delete('/{id}/', status_code=status.HTTP_204_NO_CONTENT)
def delete_task(id: int):
    if id in fake_data:
        fake_data.pop(id)
        return
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='Задача не была найдена'
    )
