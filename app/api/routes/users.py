from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select

from app.api.deps import CurrentUser, SessionDep
from app.models.user import User
from app.schemas.user import UserCreate, UserRead
from app.services.user import register_user

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register(
    session: SessionDep,
    user_reg: UserCreate,
):
    return await register_user(session=session, user_reg=user_reg)


@router.get("/me", response_model=UserRead)
async def get_me(current_user: CurrentUser):
    return current_user


@router.get("/", response_model=list[UserRead])
async def get_users(
    session: SessionDep,
    skip: int = 0,
    limit: int = 20,
):
    result = await session.execute(
        select(User).order_by(User.id).offset(skip).limit(limit)
    )
    return list(result.scalars().all())


@router.get("/{user_id}", response_model=UserRead)
async def get_user_by_id(
    session: SessionDep,
    user_id: int,
):
    user = await session.get(User, user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return user
