from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.client import Client
from app.schemas.client import ClientCreate, ClientRead, ClientUpdate


async def create_client(
    *,
    session: AsyncSession,
    client_data: ClientCreate,
    user_id: int,
) -> Client:
    client = Client(
        email=client_data.email,
        full_name=client_data.full_name,
        phone=client_data.phone,
        address=client_data.address,
        user_id=user_id,
    )

    session.add(client)
    await session.commit()
    await session.refresh(client)

    return client


async def read_client(
    *,
    session: AsyncSession,
    user_id: int,
    client_id: int,
) -> Client:
    result = await session.execute(
        select(Client).where(Client.id == client_id, Client.user_id == user_id)
    )
    client = result.scalar_one_or_none()

    if client is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found",
        )

    return client


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
    client = await read_client(
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
    client = await read_client(session=session, user_id=user_id, client_id=client_id)

    await session.delete(client)
    await session.commit()
