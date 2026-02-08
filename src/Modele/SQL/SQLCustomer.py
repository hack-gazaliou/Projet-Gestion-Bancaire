from Modele.SQL.SQLManager import Base
from sqlalchemy import Column, Integer, String
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Modele.Customer import Customer as CustomerStorageModel


class Customer(Base):
    __tablename__ = "customers"

    customer_id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    phone = Column(String(12), nullable=False)
    email = Column(String(50), nullable=False)
    card_number = Column(String(16), nullable=False)
    address = Column(String(200))

    def to_domain(self) -> "CustomerStorageModel":
        """
        Convertit les parametres SQL en un objet Customer utilisable par l'application
        C'est à dire diviser en personal_info, contact_info, card_info, etc.
        """
        from Modele.Customer import (
            Customer,
            CustomerPersonalInfo,
            CustomerContactInfo,
            CustomerCardInfo,
        )

        personal = CustomerPersonalInfo(self.first_name, self.last_name)
        contact = CustomerContactInfo(self.phone, self.email)
        card = CustomerCardInfo(self.card_number)

        return Customer(
            personal_info=personal,
            contact_info=contact,
            card_info=card,
            address=self.address,
            customer_id=self.customer_id,
        )
