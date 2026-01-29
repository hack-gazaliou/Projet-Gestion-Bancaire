from Modele.SQLManager import Base, SessionLocal
from sqlalchemy import create_engine, Column, Integer, Float, Enum
from sqlalchemy.orm import declarative_base, sessionmaker
from Modele.Operation import Operation
from enum import IntEnum


DECOUVERT_MAX = 100_000 #en centimes

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
            # Opérations où ce compte est la CIBLE (crédit)
            credits = session.query(Operation).filter_by(id_compte_cible=self.id).all()
            total_credits = sum(op.montant for op in credits)

            # Opérations où ce compte est la SOURCE (débit)
            debits = session.query(Operation).filter_by(id_compte_source=self.id).all()
            total_debits = sum(op.montant for op in debits)

            return total_credits - total_debits
        
    @classmethod
    def creer(cls, type_enum, solde_initial=0.0):
        """
        Crée le compte et, si un solde initial est fourni, 
        génère une opération technique de dépôt initial.
        """
        with SessionLocal() as session:
            nouveau = cls(type_compte=type_enum)
            session.add(nouveau)
            session.commit()
            session.refresh(nouveau)
            
            if solde_initial != 0:
                # On crée une opération "système" (ex: source ID 0 ou 9999)
                # pour simuler le dépôt initial
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
        """Récupère un objet compte par son ID."""
        with SessionLocal() as session:
            return session.query(cls).filter_by(id=compte_id).first()

    # --- MÉTHODES D'INSTANCE ---

    def sauvegarder(self):
        """Met à jour l'état actuel de l'objet en base de données."""
        with SessionLocal() as session:
            session.merge(self) # Fusionne l'objet actuel avec la session
            session.commit()
            print(f"Compte {self.id} mis à jour.")

    def supprimer(self):
        """Supprime l'instance actuelle de la base de données."""
        with SessionLocal() as session:
            objet_a_supprimer = session.query(Compte).get(self.id)
            if objet_a_supprimer:
                session.delete(objet_a_supprimer)
                session.commit()
                print(f"Compte {self.id} supprimé.")

    def __repr__(self):
        return f"<Compte(id={self.id}, type={self.type_compte.name}, solde={self.solde}€)>"