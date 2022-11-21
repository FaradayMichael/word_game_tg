import datetime
from typing import Optional

from misc import db
from models.users import User

TABLE = "users"


async def create_user(
        conn: db.Connection,
        user: User
) -> Optional[User]:
    if user.ctime is None:
        user.ctime = datetime.datetime.now()
    result = await db.create(conn, TABLE, user.dict())
    return db.record_to_model(User, result)


async def get_user(
        conn: db.Connection,
        user_id: int
) -> Optional[User]:
    values = [user_id]
    query = f'SELECT * FROM {TABLE} WHERE user_id = $1'
    result = await conn.fetchrow(query, *values)
    return db.record_to_model(User, result)
