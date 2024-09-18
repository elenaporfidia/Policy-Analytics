from sqlalchemy import create_engine, Table
from sqlalchemy.exc import SQLAlchemyError, OperationalError, DBAPIError
from sqlalchemy.orm import declarative_base, sessionmaker

from db_config import DB_USER_NAME, DB_USER_PASSWORD, DB_HOST, DB_PORT, DB_NAME

DATABASE_URL = f"mysql+pymysql://{DB_USER_NAME}:{DB_USER_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
Base = declarative_base()


def getSession():
    try:
        engine = create_engine(DATABASE_URL)
        connection = engine.connect()
        connection.close()
        session = sessionmaker(bind=engine)
        return session()
    except (OperationalError, DBAPIError):
        print("Database connection failed")
        exit()
    except Exception as e:
        print(f"Error occurred: {e}")
