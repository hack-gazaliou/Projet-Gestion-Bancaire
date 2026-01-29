from __future__ import annotations
from datetime import date
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    # Cet import n'est lu que par VS Code
    # Il sera ignoré par Python à l'exécution
    from Modele.Class_SQL.Customer_SQL import Customer as CustomerSQL

class CustomerPersonalInfo:
    def __init__(self, first_name: str, last_name: str):
        self.first_name = first_name
        self.last_name = last_name

class CustomerContactInfo:
    def __init__(self, phone: str, email: str):
        self.phone = phone
        self.email = email

class CustomerCardInfo:
    def __init__(self, card_number: str, expire_date: date):
        self.card_number = card_number
        self.expire_date = expire_date


class Customer:
    def __init__(self, personal_info: CustomerPersonalInfo, contact_info: CustomerContactInfo, 
                 card_info: CustomerCardInfo, address: str, customer_id: int = None):
        self.customer_id = customer_id
        self.personal_info = personal_info
        self.contact_info = contact_info
        self.card_info = card_info
        self.address = address

    def save(self, session):
        """
        Crée un nouveau Customer si l'ID est absent, ou met à jour l'existante
        """
        from sqlalchemy.exc import SQLAlchemyError
        from Modele.Class_SQL.Customer_SQL import Customer as CustomerSQL  
        # Import local pour éviter une erreur ImportError ou AttributeError
        # car classe Customer_SQL importe aussi Customer
        
        customer_storage_model = CustomerSQL(
            customer_id=self.customer_id,
            first_name=self.personal_info.first_name,
            last_name=self.personal_info.last_name,
            phone=self.contact_info.phone,
            email=self.contact_info.email,
            card_number=self.card_info.card_number,
            expire_date=self.card_info.expire_date,
            address=self.address
        )

        if self.customer_id is None:
            action_name = "créé"
        else:
            action_name = "mis à jour"
        
        try:
            customer_storage_model = session.merge(customer_storage_model)
            session.commit()
            
            self.synchro_id_from_storage(customer_storage_model)
            print(f"Le client {self.personal_info.first_name} a été {action_name} avec succès (ID: {self.customer_id}).")
            
        except SQLAlchemyError as database_error:
            session.rollback()
            print(f"Erreur SQL critique : {database_error}")

    def synchro_id_from_storage(self, customer_storage_model: CustomerSQL):
        """Met à jour l'ID de l'objet Customer avec celui généré par la BDD"""
        self.customer_id = customer_storage_model.customer_id

    @classmethod
    def obtain(cls, session, customer_id_to_obtain: int) -> Customer | None:
        """
        Récupère un client dans la bdd et reconstruit l'objet Customer
        """
        from sqlalchemy.exc import SQLAlchemyError
        from Modele.Class_SQL.Customer_SQL import Customer as CustomerSQL
        
        try:
            customer_storage_model: CustomerSQL | None = session.query(CustomerSQL).filter_by(
                customer_id=customer_id_to_obtain
            ).first()
        except SQLAlchemyError as database_error:
            print(f"Erreur lors de la récupération du client {customer_id_to_obtain} : {database_error}")
            return None

        if customer_storage_model:
            personal: CustomerPersonalInfo = CustomerPersonalInfo(
                first_name=customer_storage_model.first_name, 
                last_name=customer_storage_model.last_name
            )
            contact: CustomerContactInfo = CustomerContactInfo(
                phone=customer_storage_model.phone, 
                email=customer_storage_model.email
            )
            card: CustomerCardInfo = CustomerCardInfo(
                card_number=customer_storage_model.card_number, 
                expire_date=customer_storage_model.expire_date
            )
            return cls(
                personal_info=personal,
                contact_info=contact,
                card_info=card,
                address=customer_storage_model.adress,
                customer_id=customer_storage_model.customer_id
            )
        return None

    def remove(self, session):
        """
        Supprime le client actuel de la base de données
        """
        from sqlalchemy.exc import SQLAlchemyError
        from Modele.Class_SQL.Customer_SQL import Customer as CustomerSQL

        if not self.customer_id:
            print("Action impossible : Ce client n'a pas d'ID (il n'est pas enregistré dans la base).")
            return
        
        try:
            customer_storage_model: CustomerSQL | None = session.query(CustomerSQL).filter_by(
            customer_id=self.customer_id
        ).first()
        except SQLAlchemyError as search_error:
            print(f"Erreur lors de la recherche : {search_error}")
            return
        
        if not customer_storage_model:
            print(f"Le client {self.customer_id} n'existe pas en base.")
            return

        try:
            session.delete(customer_storage_model)
            session.commit()
        except SQLAlchemyError as delete_error:
            session.rollback()
            print(f"Erreur lors de la suppression : {delete_error}")
            return
        
        print(f"Le client {self.personal_info.first_name} a été supprimé avec succès (ID: {self.customer_id}).")
        self.reset_id()

    def reset_id(self):
        """
        Détache l'objet Customer de son id en base de données
        Utile après une suppression ou pour cloner un client
        """
        self.customer_id = None