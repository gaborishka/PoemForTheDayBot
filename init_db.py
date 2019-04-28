from sqlalchemy import create_engine, MetaData
from poem_for_the_day_bot.db import users
import os

DSN = "postgresql://{user}:{password}@{host}:{port}/{database}"


def create_tables(engine):
    meta = MetaData()
    meta.create_all(bind=engine, tables=[users])


def drop_tables(engine):
    meta = MetaData()
    meta.drop_all(bind=engine, tables=[users])


def sample_data(engine):
    conn = engine.connect()
    conn.execute(users.insert(), [
        {
            'id': 132341234,
            'username': 'test@mail.com',
            'first_name': 'Test',
            'last_name': 'User',
        }
    ])

    conn.close()


if __name__ == '__main__':

    db_url = DSN.format(
        user=os.environ['POSTGRES_USER'],
        password=os.environ['POSTGRES_PASSWORD'],
        host=os.environ['POSTGRES_HOST'],
        port=os.environ['POSTGRES_PORT'],
        database=os.environ['POSTGRES_DB'],
    )
    engine = create_engine(db_url)

    create_tables(engine)
    sample_data(engine)
    print(engine.execute(users.select()).first())
