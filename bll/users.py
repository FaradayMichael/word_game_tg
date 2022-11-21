from typing import Optional

from db.users import get_user, create_user
from misc import db
from models.users import User


async def get_or_create_user(
        conn: db.Connection,
        user_id: int,
        name: str = None
) -> Optional[User]:
    user = await get_user(conn, user_id)
    if user is None:
        user = await create_user(
            conn,
            User(
                user_id=user_id,
                name=name
            )
        )
    return user
