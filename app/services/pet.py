from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.client import Client
from app.models.pet import Pet
from app.schemas.pet import PetCreate
from app.services.client import read_client


async def create_pet(
    *,
    session: AsyncSession,
    pet_data: PetCreate,
    user_id: int,
    client_id: int,
) -> Pet:
    client = await read_client(session=session, user_id=user_id, client_id=client_id)

    pet = Pet(**pet_data.model_dump(), client_id=client.id)

    session.add(pet)
    await session.commit()
    await session.refresh(pet)

    return pet


# async def read_pet(
#     *,
#     session: AsyncSession,
#     client_id: int,
# ) -> Pet:
#     pass


# async def list_pets(
#     *,
#     session: AsyncSession,
#     client_id: int,
#     skip: int = 0,
#     limit: int = 20,
# ) -> list[Pet]:
#     pass
