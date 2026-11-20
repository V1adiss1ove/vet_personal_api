from fastapi import APIRouter

from app.api.deps import SessionDep
from app.schemas.token import TokenResponse
from app.schemas.user import UserAuthenticate
from app.services.user import authenticate

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/", response_model=TokenResponse)
async def login(
    session: SessionDep,
    user_auth: UserAuthenticate,
):
    return await authenticate(session=session, user_auth=user_auth)
