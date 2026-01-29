from Modele.SQLManager import Base, SessionLocal
from sqlalchemy import ForeignKey, Column, Integer, String, Date
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import date



class Customer(Base):
    __tablename__ = 'customers'

    customer_id = Column(Integer, primary_keys = True, autoincrement = True)
    first_name = Column(String(50), nullable = False)
    last_name = Column(String(50), nullable = False)
    phone = Column(String(12), nullable = False)
    email = Column(String(50), nullable = False)
    number = Column(String(16), nullable=False)
    expire_date = Column(Date, nullable=False)
    adress = Column(String(200))



    