from typing import Optional, Union

from fastapi import Depends, Request
from fastapi_users import (BaseUserManager, FastAPIUsers, IntegerIDMixin,
                           InvalidPasswordException)
from fastapi_users.authentication import (AuthenticationBackend,
                                          BearerTransport, JWTStrategy)
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.db import get_async_session
from app.models.user import User
from app.schemas.user import UserCreate


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)


bearer_transport = BearerTransport(tokenUrl='auth/jwt/login')


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(settings.secret, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name='jwt',
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    async def validate_password(
        self, password: str,
        user: Union[UserCreate, User],
    ) -> None:
        if len(password) < 6:
            raise InvalidPasswordException(
                reason='Password must be at leat 6 characters'
            )
        if user.email in password:
            raise InvalidPasswordException(
                reason='Password cannot contain email'
            )

    async def on_after_register(
        self, user: User,
        request: Optional[Request] = None
    ) -> None:
        print(f'Пользователь {user.email} зарегистрирован.')
        return


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)

fastapi_users = FastAPIUsers[User, int](get_user_manager, [auth_backend])
current_user = fastapi_users.current_user(active=True)
current_admin = fastapi_users.current_user(active=True, superuser=True)
