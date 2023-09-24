from os import environ
from dotenv import load_dotenv
from sqlmodel import SQLModel, create_engine

load_dotenv()

database_url = f"postgresql://{environ.get('DB_USER')}:{environ.get('DB_PASSWORD')}@{environ.get('DB_HOST')}/{environ.get('DB_NAME')}"

engine = create_engine(database_url)


def init_database():
    SQLModel.metadata.create_all(engine)
