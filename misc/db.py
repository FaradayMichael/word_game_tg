import logging
import datetime
from typing import (
    Optional,
    Any,
    List,
    Dict,
    Union,
    Type
)
import asyncpg
import json
from pydantic import BaseModel

logger = logging.getLogger(__name__)

Connection = asyncpg.Connection


async def init(config: dict) -> asyncpg.Pool:
    dsn = config.get('dsn')
    if not dsn:
        raise RuntimeError('DB connection parameters not defined')
    return await asyncpg.create_pool(
        dsn,
        init=init_connection,
        **{k: v for k, v in config.items() if k != 'dsn'}
    )


async def get_conn(config: dict) -> Connection:
    dsn = config.pop('dsn')
    if not dsn:
        raise RuntimeError('DB connection parameters not defined')
    return await asyncpg.connect(dsn, **config)


async def close(db: Union[asyncpg.Pool, asyncpg.Connection]):
    await db.close()


async def init_connection(conn):
    await conn.set_type_codec(
        'jsonb',
        encoder=json.dumps,
        decoder=json.loads,
        schema='pg_catalog'
    )
    return conn


async def get_by_where(
        conn: Connection,
        table: str,
        where: str,
        values: Optional[List] = [],
        fields: Optional[List[str]] = None
) -> Optional[asyncpg.Record]:
    select_fields = ', '.join(fields) if fields else '*'
    query = f'SELECT {select_fields} FROM {table} WHERE {where}'
    try:
        return await conn.fetchrow(query, *values)
    except:
        logger.exception(f'Query {query} failed')
        raise


def record_to_model_list(model_cls: Type[BaseModel], records: List[asyncpg.Record]) -> List[Type[BaseModel]]:
    if records:
        return [record_to_model(model_cls, i) for i in records]
    return []


def record_to_model(model_cls: Type[BaseModel], record: Optional[asyncpg.Record]) -> Optional[Type[BaseModel]]:
    if record:
        return model_cls.parse_obj(record)
    return None


async def get(
        conn: Connection,
        table: str,
        pk: int,
        fields: Optional[List[str]] = None
) -> Optional[asyncpg.Record]:
    select_fields = ', '.join(fields) if fields else '*'
    query = f'SELECT {select_fields} FROM {table} WHERE id = $1'
    try:
        return await conn.fetchrow(query, pk)
    except:
        logger.exception(f'Query {query} failed')
        raise


async def get_list(
        conn: Connection,
        table: str,
        where: str,
        values: Optional[List] = [],
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        order: Optional[List[str]] = None,
        fields: Optional[List[str]] = [],
) -> List[asyncpg.Record]:
    select_fields = ', '.join(fields) if fields else '*'
    where_query, limit_query, offset_query, order_query = '', '', '', ''
    if where:
        where_query = f'WHERE {where}'
    if limit:
        limit_query = f'LIMIT {limit}'
    if offset:
        offset_query = f'OFFSET {offset}'
    if order:
        order_query = 'ORDER BY ' + ', '.join([f'{i} DESC' if i.startswith('-') else i for i in order])

    query = f'SELECT {select_fields} FROM {table} {where_query} {order_query} {limit_query} {offset_query}'
    try:
        return await conn.fetch(query, *values)
    except:
        logger.exception(f'Query {query} {values} failed')
        raise


async def create(
        conn: Connection,
        table: str,
        data: Dict[str, Any],
        insert_fields: Optional[List[str]] = None,
        ignore_fields: Optional[List[str]] = None,
        fields: Optional[List[str]] = []
) -> Optional[asyncpg.Record]:
    return_fields = ', '.join(fields) if fields else '*'
    field_names = []
    placeholders = []
    values = []
    idx = 1
    for key in data.keys():
        if insert_fields and key not in insert_fields:
            continue

        if ignore_fields and key in ignore_fields:
            continue

        field_names.append(key)
        placeholders.append(f"${idx}")
        values.append(data[key])
        idx += 1
    query = f'INSERT INTO {table} ({", ".join(field_names)}) VALUES ({", ".join(placeholders)}) RETURNING {return_fields}'
    try:
        return await conn.fetchrow(query, *values)
    except:
        logger.exception(f'Query {query} failed')
        raise


async def insert_many(
        conn: Connection,
        table: str,
        data: List[dict],
        insert_fields: List[str] = []
) -> None:
    if not data:
        return
    values = []
    insert_fields = insert_fields if insert_fields else [field for field in data[0]]
    for item in data:
        item_values = []
        for field in insert_fields:
            item_values.append(item.get(field))
        values.append(item_values)
    str_insert_fields = ", ".join(insert_fields)
    placeholders = ", ".join([f"${i + 1}" for i in range(len(insert_fields))])
    query = f'INSERT INTO {table} ({str_insert_fields}) VALUES ({placeholders})'
    try:
        await conn.executemany(query, values)
    except Exception:
        logger.exception(f'Query {query} failed')
        raise


async def update(
        conn: Connection,
        table: str,
        pk: int,
        data: Dict[str, Any],
        update_fields: Optional[List[str]] = None,
        ignore_fields: Optional[List[str]] = None,
        fields: Optional[List[str]] = [],
        with_atime: bool = False
) -> Optional[asyncpg.Record]:
    return_fields = ', '.join(fields) if fields else '*'
    placeholders = []
    values = []
    idx = 1
    for key in data.keys():
        if with_atime and key == 'atime':
            continue

        if update_fields and key not in update_fields:
            continue

        if ignore_fields and key in ignore_fields:
            continue

        placeholders.append(f"{key} = ${idx}")
        values.append(data[key])
        idx += 1
    if with_atime:
        placeholders.append(f"atime = (now() at time zone 'utc')")
    update = ', '.join(placeholders)
    query = f'UPDATE {table} SET {update} WHERE id = ${len(values) + 1} RETURNING {return_fields}'
    values.append(pk)
    try:
        return await conn.fetchrow(query, *values)
    except:
        logger.exception(f'Query {query} failed')
        raise
