from psycopg2 import connect
import pytest
import psycopg2


@pytest.fixture
def get_connection():
    conn = None
    try:
        conn = connect(
            host="localhost",
            database="suppliers",
            user="root",
            password="password")
        cur = conn.cursor()
        yield cur
        cur.close()
        conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        if conn is not None:
            conn.close()


@pytest.fixture(scope='class')
def init_db():
    conn = None
    try:
        conn = connect(
            host="localhost",
            database="suppliers",
            user="root",
            password="password")
        cur = conn.cursor()
        cur.execute(open("init.sql", "r").read())
        print('------')
        print("Init db is Done")
        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()