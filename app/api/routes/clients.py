from typing import Annotated

from fastapi import APIRouter, Query, status

from app.api.deps import CurrentUser, SessionDep
from app.schemas.client import ClientCreate, ClientRead, ClientUpdate
from app.services import client as client_service

router = APIRouter(prefix="/clients", tags=["Clients"])


@router.get("/", response_model=list[ClientRead])
async def list_clients(
    session: SessionDep,
    current_user: CurrentUser,
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(gt=0, le=100)] = 20,
):
    return await client_service.list_clients(
        session=session,
        user_id=current_user.id,
        skip=skip,
        limit=limit,
    )


@router.post("/", response_model=ClientRead, status_code=status.HTTP_201_CREATED)
async def create_client(
    session: SessionDep,
    client_data: ClientCreate,
    current_user: CurrentUser,
):
    return await client_service.create_client(
        session=session,
        client_data=client_data,
        user_id=current_user.id,
    )


@router.get("/{client_id}", response_model=ClientRead)
async def get_client(
    session: SessionDep,
    client_id: int,
    current_user: CurrentUser,
):
    return await client_service.read_client(
        session=session,
        user_id=current_user.id,
        client_id=client_id,
    )


@router.patch("/{client_id}", response_model=ClientRead)
async def update_client(
    session: SessionDep,
    client_data: ClientUpdate,
    client_id: int,
    current_user: CurrentUser,
):
    return await client_service.update_client(
        session=session,
        client_update=client_data,
        client_id=client_id,
        user_id=current_user.id,
    )


@router.delete("/{client_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_client(
    session: SessionDep,
    client_id: int,
    current_user: CurrentUser,
):
    return await client_service.delete_client(
        session=session,
        client_id=client_id,
        user_id=current_user.id,
    )
