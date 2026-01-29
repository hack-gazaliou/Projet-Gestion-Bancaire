from enum import IntEnum
from Modele.SQL.SQLComptes import SQLCompte
import logging

logger = logging.getLogger(__name__)

class TypeCompte(IntEnum):
    COURANT = 0
    LIVRET_A = 1
    PEL = 2

class Compte():
    def __init__(self, id : int, type_compte : TypeCompte, id_client : int, initial_amount : int = 0) -> None:
        self.type_compte = type_compte
        self.id_client = id_client
        self.id = id 
        # On ne crée en base QUE si l'id n'existe pas encore
        if self.id is None:
            # Note : Assurez-vous que SQLCompte.creer accepte un montant initial
            new = SQLCompte.creer(self.type_compte, self.id_client,initial_amount) 
            self.id = new.id

    @property
    def solde(self) -> int:
        """Calcule le solde actuel en sommant toutes les opérations."""
        with SessionLocal() as session:
            # Opérations cibles
            credits = session.query(Operation).filter_by(id_compte_cible=self.id).all()
            total_credits = sum(op.montant for op in credits)

            # Opérations sources
            debits = session.query(Operation).filter_by(id_compte_source=self.id).all()
            total_debits = sum(op.montant for op in debits)
            return total_credits - total_debits
        
    @classmethod
    def load(cls, account_id):
        """
        Load an account based on the id
        """
        account = SQLCompte.get(account_id)
        if not account:
            logger.error(f"Account not found")
            return None
        loaded_account = cls(id = account.id, type_compte = account.type_compte, id_client = account.id_client)

    @classmethod
    def obtenir(cls, compte_id):
        """Récupère un objet compte par son ID"""
        with SessionLocal() as session:
            return session.query(cls).filter_by(id=compte_id).first()

    def sauvegarder(self):
        """Met à jour l'état actuel de l'objet en base de données"""
        with SessionLocal() as session:
            session.merge(self) # fusionner l'objet actuel avec la session
            session.commit()
            logger.debug(f"Account {self.id} updated")

    def supprimer(self):
        """Supprime l'instance actuelle de la base de données"""
        with SessionLocal() as session:
            objet_a_supprimer = session.query(Compte).get(self.id)
            if objet_a_supprimer:
                session.delete(objet_a_supprimer)
                session.commit()
                logger.debug(f"Account {self.id} deleted")

    def __repr__(self):
        return f"<Compte(id={self.id}, type={self.type_compte.name}, solde={self.solde}€)>"