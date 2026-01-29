from Modele.SQLManager import Base, SessionLocal
from sqlalchemy import Column, Integer, Enum
from Modele.Operation import Operation
from enum import IntEnum
import logging

logger = logging.getLogger(__name__)

class TypeCompte(IntEnum):
    COURANT = 0
    LIVRET_A = 1
    PEL = 2

class Compte(Base):
    __tablename__ = 'comptes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    type_compte = Column(Enum(TypeCompte), default=TypeCompte.COURANT)
    #solde = Column(Float, default=0.0)

    @property
    def solde(self):
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
    def creer(cls, type_enum, solde_initial=0.0):
        """
        Crée le compte et, si un solde initial est fourni, 
        génère une opération de dépôt initial
        """
        with SessionLocal() as session:
            nouveau = cls(type_compte=type_enum)
            session.add(nouveau)
            session.commit()
            session.refresh(nouveau)
            
            if solde_initial != 0:
                # Simulation dépot initial pour faire les transactions de création de compte
                from Modele.Operation import Operation
                op_initiale = Operation(
                    id_compte_source=0, # 0 = Coffre-fort de la banque
                    id_compte_cible=nouveau.id,
                    montant=solde_initial
                )
                session.add(op_initiale)
                session.commit()
            
            return nouveau
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