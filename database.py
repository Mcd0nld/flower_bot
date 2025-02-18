from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL

# подключение к бд
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)

# базовый класс моделей
Base = declarative_base()

# модель клиента
class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    birth_date = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)

# создание таблиц в бд
Base.metadata.create_all(engine)