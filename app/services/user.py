from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import encode_token, hash_password, verify_password
from app.models.user import User
from app.schemas.token import TokenResponse
from app.schemas.user import UserAuthenticate, UserCreate


async def get_user_by_email(*, session: AsyncSession, email: str) -> User | None:
    result = await session.execute(select(User).where(User.email == email))

    return result.scalar_one_or_none()


async def register_user(
    *,
    session: AsyncSession,
    user_reg: UserCreate,
) -> User:
    existing_user = await get_user_by_email(session=session, email=user_reg.email)

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="The user with this email already exists in the system",
        )

    hashed_password = hash_password(user_reg.password).decode()  # bytes -> str

    user = await create_user(
        session=session,
        user_create=user_reg,
        hashed_password=hashed_password,
    )

    return user


async def create_user(
    *,
    session: AsyncSession,
    user_create: UserCreate,
    hashed_password: str,
) -> User:

    user = User(
        email=user_create.email,
        hashed_password=hashed_password,
        full_name=user_create.full_name,
    )

    session.add(user)
    await session.commit()
    await session.refresh(user)

    return user


async def authenticate(
    *,
    session: AsyncSession,
    user_auth: UserAuthenticate,
) -> TokenResponse:
    user = await get_user_by_email(session=session, email=user_auth.email)

    if not user or not verify_password(
        password=user_auth.password,
        hashed_password=user.hashed_password,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is inactive",
        )
    token = encode_token(subject=user.id)

    return TokenResponse(access_token=token)
