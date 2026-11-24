from fastapi import APIRouter, status

from app.api.deps import SessionDep
from app.schemas.token import TokenResponse
from app.schemas.user import UserAuthenticate, UserCreate, UserRead
from app.services import user as service_user

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=TokenResponse)
async def login(
    session: SessionDep,
    user_auth: UserAuthenticate,
):
    return await service_user.authenticate(session=session, user_auth=user_auth)


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register(
    session: SessionDep,
    user_reg: UserCreate,
):
    return await service_user.register_user(session=session, user_reg=user_reg)
