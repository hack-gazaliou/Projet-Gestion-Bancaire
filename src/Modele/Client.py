from Modele.SQLManager import Base, SessionLocal
from sqlalchemy import ForeignKey, Column, Integer, String, Date
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import date
import calendar


class CustomerPersonalInfo(Base):
    __tablename__ = 'customer_personal_info'

    first_name = Column(String(50), nullable = False)
    last_name = Column(String(50), nullable = False)


class CustomerContactInfo(Base):
    __tablename__ = 'customer_contact_info'

    phone = Column(String(12), nullable = False)
    email = Column(String(50), nullable = False)


class CustomerCardInfo(Base):
    __tablename__ = 'customer_card_info'

    number = Column(String(16))
    expiration_date = Column(Date, nullable=True)

    def set_expiration(self, month: int, year: int):
        """Stocke la date au dernier jour du mois d'expiration."""
        last_day = calendar.monthrange(year, month)[1]
        self.expiration_date = date(year, month, last_day)


class Customer(Base):
    __tablename__ = 'customers'

    id = Column(Integer, primary_keys = True, autoincrement = True)
    adresse = Column(String(200))

    personal_info: CustomerPersonalInfo
    contact_info: CustomerContactInfo
    card_info: CustomerCardInfo