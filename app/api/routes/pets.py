from typing import Annotated

from fastapi import APIRouter, Query, status

from app.api.deps import CurrentUser, SessionDep
from app.schemas.pet import PetCreate, PetRead, PetUpdate
from app.services import pet as pet_service

router = APIRouter(prefix="clients/{client_id}/pets", tags=["Pets"])


@router.post("/", response_model=PetRead, status_code=status.HTTP_201_CREATED)
async def create_pet(
    session: SessionDep,
    pet_data: PetCreate,
    client_id: int,
    current_user: CurrentUser,
):
    return await pet_service.create_pet(
        session=session,
        pet_data=pet_data,
        client_id=client_id,
        user_id=current_user.id,
    )


@router.get("/", response_model=list[PetRead])
async def list_pets(
    session: SessionDep,
    client_id: int,
    current_user: CurrentUser,
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(gt=0, le=100)] = 20,
):
    return await pet_service.list_pets(
        session=session,
        client_id=client_id,
        user_id=current_user.id,
        skip=skip,
        limit=limit,
    )


@router.get("/{pet_id}", response_model=PetRead)
async def get_pet(
    session: SessionDep,
    client_id: int,
    pet_id: int,
    current_user: CurrentUser,
):
    return await pet_service.read_pet(
        session=session,
        client_id=client_id,
        user_id=current_user.id,
        pet_id=pet_id,
    )


@router.patch("/{pet_id}", response_model=PetRead)
async def update_pet(
    session: SessionDep,
    pet_data: PetUpdate,
    client_id: int,
    pet_id: int,
    current_user: CurrentUser,
):
    return await pet_service.update_pet(
        session=session,
        pet_update=pet_data,
        client_id=client_id,
        user_id=current_user.id,
        pet_id=pet_id,
    )


@router.delete("/{pet_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_pet(
    session: SessionDep,
    client_id: int,
    pet_id: int,
    current_user: CurrentUser,
):
    await pet_service.delete_pet(
        session=session,
        client_id=client_id,
        user_id=current_user.id,
        pet_id=pet_id,
    )
