from Modele.SQL.SQLManager import Base, SessionLocal
from sqlalchemy import Column, Integer, Enum, ForeignKey
from Modele.SQL.SQLOperations import SQLOperation
from Modele.Compte import TypeCompte
import logging

logger = logging.getLogger(__name__)


class SQLCompte(Base):
    __tablename__ = "comptes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    type_compte = Column(Enum(TypeCompte), default=TypeCompte.COURANT, nullable=False)
    id_client = Column(Integer, ForeignKey("customers.id"), nullable=False)

    @classmethod
    def get_credits_and_debits(cls, account_id: int | Column[int]) -> tuple[int, int]:
        with SessionLocal() as session:
            credits = session.query(cls).filter_by(id_compte_cible=account_id).all()
            total_credits = sum(op.montant for op in credits)
            debits = (
                session.query(SQLOperation).filter_by(id_compte_source=account_id).all()
            )
            total_debits = sum(op.montant for op in debits)
            return total_credits, total_debits  # type: ignore

    @classmethod
    def creer(cls, type_enum, id_client, initial_amount: int = 0):
        """
        Creates the account and, if an initial balance is provided,
        generates an initial deposit transaction.
        """
        with SessionLocal() as session:
            nouveau = cls(type_compte=type_enum, id_client=id_client)
            session.add(nouveau)
            session.commit()
            session.refresh(nouveau)

            if initial_amount != 0:
                # Initial deposit transaction when opening an account
                from Modele.Operation import Operation

                op_initiale = Operation(
                    id_source_account=0,  # Primary account (of the bank)
                    id_target_account=nouveau.id,  # type: ignore
                    amount=initial_amount,
                )
                Operation.execute(op_initiale)

            return nouveau

    @classmethod
    def get(cls, compte_id):
        """Get an account by it's id"""
        with SessionLocal() as session:
            return session.query(cls).filter_by(id=compte_id).first()

    def sauvegarder(self):
        """Update the account in the database"""
        with SessionLocal() as session:
            session.merge(self)
            session.commit()
            logger.debug(f"Account {self.id} updated")

    def supprimer(self):
        """Delete the account from the database"""
        with SessionLocal() as session:
            objet_a_supprimer = session.query(SQLOperation).get(self.id)
            if objet_a_supprimer:
                session.delete(objet_a_supprimer)
                session.commit()
                logger.debug(f"Account {self.id} deleted")

    def __repr__(self):
        return (
            f"<Compte(id={self.id}, type={self.type_compte.name}, solde={self.solde}€)>"
        )
