import aiopg.sa
import os
from sqlalchemy import (
    MetaData, Table, Column,
    BigInteger, String, Time
)
from sqlalchemy import create_engine

meta = MetaData()

users = Table(
    'users', meta,

    Column('id', BigInteger, primary_key=True),
    Column('username', String(100), nullable=False),
    Column('first_name', String(100), nullable=False),
    Column('last_name', String(100), nullable=False),
    Column('time', Time, nullable=True)
)


class RecordNotFound(Exception):
    """Requested record in database was not found"""


async def init_pg(app):
    engine = await aiopg.sa.create_engine(
        user=os.environ['POSTGRES_USER'],
        password=os.environ['POSTGRES_PASSWORD'],
        host=os.environ['POSTGRES_HOST'],
        port=os.environ['POSTGRES_PORT'],
        database=os.environ['POSTGRES_DB'],
        minsize=int(os.environ['POSTGRES_MIN_SIZE']),
        maxsize=int(os.environ['POSTGRES_MAX_SIZE']),
    )
    app['db'] = engine


async def close_pg(app):
    app['db'].close()
    await app['db'].wait_closed()


async def get_user(conn, user_id):
    result = await conn.execute(
        users.select().where(users.c.id == user_id)
    )
    user_record = await result.first()

    if not user_record:
        msg = "User with id: {} does not exists"
        raise RecordNotFound(msg.format(user_id))

    return user_record


async def get_users(conn):
    records = await conn.execute(
        users.select().order_by(users.c.id)
    )
    print(records)
    return records
