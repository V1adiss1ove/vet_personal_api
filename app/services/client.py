from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.client import Client
from app.schemas.client import ClientCreate, ClientUpdate


async def create_client(
    *,
    session: AsyncSession,
    client_data: ClientCreate,
    user_id: int,
) -> Client:
    client = Client(**client_data.model_dump(), user_id=user_id)

    session.add(client)
    await session.commit()
    await session.refresh(client)

    return client


async def get_client_for_user(
    *,
    session: AsyncSession,
    user_id: int,
    client_id: int,
):
    client = await session.get(Client, client_id)

    if client is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Client not found"
        )

    if client.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions"
        )

    return client


async def read_client(
    *,
    session: AsyncSession,
    user_id: int,
    client_id: int,
) -> Client:

    return await get_client_for_user(
        session=session,
        user_id=user_id,
        client_id=client_id,
    )


async def list_clients(
    *,
    session: AsyncSession,
    user_id: int,
    skip: int = 0,
    limit: int = 20,
) -> list[Client]:
    stmt = (
        select(Client)
        .where(Client.user_id == user_id)
        .order_by(Client.created_at.desc())
        .offset(skip)
        .limit(limit)
    )

    result = await session.execute(stmt)

    return result.scalars().all()


async def update_client(
    *,
    session: AsyncSession,
    client_update: ClientUpdate,
    client_id: int,
    user_id: int,
) -> Client:
    client = await get_client_for_user(
        session=session,
        user_id=user_id,
        client_id=client_id,
    )
    for field, value in client_update.model_dump(exclude_unset=True).items():
        setattr(client, field, value)

    await session.commit()
    await session.refresh(client)

    return client


async def delete_client(
    *,
    session: AsyncSession,
    client_id: int,
    user_id: int,
) -> None:
    client = await get_client_for_user(
        session=session,
        user_id=user_id,
        client_id=client_id,
    )

    await session.delete(client)
    await session.commit()
