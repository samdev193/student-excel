from sqlalchemy.orm import declarative_base, sessionmaker, Session
from sqlalchemy import create_engine
from decouple import config
user = config('DB_USER')
password = config('DB_PASSWORD')
db_name = config('DB_NAME')
host = config('DB_HOST')

engine = create_engine(f"postgresql://{user}:{password}@{host}:5432/{db_name}",echo=True)

Base = declarative_base()

SessionLocal: sessionmaker=sessionmaker(bind=engine)

