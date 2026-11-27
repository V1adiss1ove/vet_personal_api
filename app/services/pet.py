from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.pet import Pet
from app.schemas.pet import PetCreate, PetUpdate
from app.services.client import get_client_for_user


async def create_pet(
    *,
    session: AsyncSession,
    pet_data: PetCreate,
    user_id: int,
    client_id: int,
) -> Pet:
    client = await get_client_for_user(
        session=session,
        user_id=user_id,
        client_id=client_id,
    )

    pet = Pet(**pet_data.model_dump(), client_id=client.id)

    session.add(pet)
    await session.commit()
    await session.refresh(pet)

    return pet


async def get_pet_for_client(
    *,
    session: AsyncSession,
    client_id: int,
    user_id: int,
    pet_id: int,
) -> Pet:
    client = await get_client_for_user(
        session=session, user_id=user_id, client_id=client_id
    )
    pet = await session.get(Pet, pet_id)

    if pet is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pet not found",
        )

    if client.id != pet.client_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )

    return pet


async def read_pet(
    *,
    session: AsyncSession,
    client_id: int,
    user_id: int,
    pet_id: int,
) -> Pet:

    return await get_pet_for_client(
        session=session,
        user_id=user_id,
        client_id=client_id,
        pet_id=pet_id,
    )


async def list_pets(
    *,
    session: AsyncSession,
    client_id: int,
    user_id: int,
    skip: int = 0,
    limit: int = 20,
) -> list[Pet]:
    client = await get_client_for_user(
        session=session,
        user_id=user_id,
        client_id=client_id,
    )

    result = await session.execute(
        select(Pet)
        .where(Pet.client_id == client.id)
        .order_by(Pet.created_at.desc())
        .offset(skip)
        .limit(limit)
    )

    return result.scalars().all()


async def update_pet(
    *,
    session: AsyncSession,
    pet_update: PetUpdate,
    client_id: int,
    user_id: int,
    pet_id: int,
) -> Pet:
    pet = await get_pet_for_client(
        session=session,
        user_id=user_id,
        client_id=client_id,
        pet_id=pet_id,
    )
    data = pet_update.model_dump(exclude_unset=True)
    if not data:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="At least one field must be provided",
        )
    for field, value in data.items():
        setattr(pet, field, value)

    await session.commit()
    await session.refresh(pet)

    return pet


async def delete_pet(
    *,
    session: AsyncSession,
    client_id: int,
    user_id: int,
    pet_id: int,
) -> None:
    pet = await get_pet_for_client(
        session=session,
        user_id=user_id,
        client_id=client_id,
        pet_id=pet_id,
    )

    await session.delete(pet)
    await session.commit()
