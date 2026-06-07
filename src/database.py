import os

from dotenv import load_dotenv
from sqlalchemy import URL, create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAMESPACE = os.getenv("DB_NAMESPACE")

# DATABASE_URL = (
#     f"iris+intersystems://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAMESPACE}"
# )
if not (DB_USER and DB_PASSWORD and DB_HOST and DB_PORT and DB_NAMESPACE):
    raise ValueError("configuração incompleta, checar arquivo de configuração ambientes.")

DATABASE_URL = URL.create(
    drivername="iris+intersystems",
    username=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=int(DB_PORT),
    database=DB_NAMESPACE,
)

engine = create_engine(DATABASE_URL, pool_pre_ping=True, connect_args={"ssl": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
