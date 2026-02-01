"""
SQL Account Management Module.
Handles database operations for bank accounts.
"""

import logging
from sqlalchemy import Column, Integer, Enum, ForeignKey

from Modele.compte import TypeCompte
from Modele.SQL.sql_manager import Base, SESSIONLOCAL
from Modele.SQL.sql_operations import SQLOperation

logger = logging.getLogger(__name__)


class SQLCompte(Base):
    """
    Represents a bank account in the database.
    """

    __tablename__ = "comptes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    type_compte = Column(Enum(TypeCompte), default=TypeCompte.COURANT, nullable=False)
    id_client = Column(Integer, ForeignKey("customers.id"), nullable=False)

    @classmethod
    def get_credits_and_debits(cls, account_id: int) -> tuple[int, int]:
        """
        Calculates the total amount of credits and debits for a specific account.
        """
        with SESSIONLOCAL() as session:
            credit_ops = session.query(cls).filter_by(id_compte_cible=account_id).all()
            total_credits = sum(op.montant for op in credit_ops)
            debit_ops = (
                session.query(SQLOperation).filter_by(id_compte_source=account_id).all()
            )
            total_debits = sum(op.montant for op in debit_ops)
            return total_credits, total_debits  # type: ignore

    @classmethod
    def creer(cls, type_enum, id_client, initial_amount: int = 0):
        """
        Creates the account and, if an initial balance is provided,
        generates an initial deposit transaction.
        """
        with SESSIONLOCAL() as session:
            nouveau = cls(type_compte=type_enum, id_client=id_client)
            session.add(nouveau)
            session.commit()
            session.refresh(nouveau)

            if initial_amount != 0:
                # pylint: disable=import-outside-toplevel
                from Modele.operation import Operation

                op_initiale = Operation(
                    id_source_account=0,  # Bank internal account
                    id_target_account=nouveau.id,  # type: ignore
                    amount=initial_amount,
                )
                Operation.execute(op_initiale)

            return nouveau

    @classmethod
    def get(cls, compte_id):
        """
        Retrieves an account by its unique identifier.
        """
        with SESSIONLOCAL() as session:
            return session.query(cls).filter_by(id=compte_id).first()

    def sauvegarder(self):
        """
        Updates the account record in the database.
        """
        with SESSIONLOCAL() as session:
            session.merge(self)
            session.commit()
            logger.debug("Account %s updated", self.id)

    def supprimer(self):
        """
        Deletes the account from the database.
        """
        with SESSIONLOCAL() as session:
            objet_a_supprimer = session.query(SQLOperation).get(self.id)
            if objet_a_supprimer:
                session.delete(objet_a_supprimer)
                session.commit()
                logger.debug("Account %s deleted", self.id)

    def __repr__(self):
        return f"<Compte(id={self.id}, type={self.type_compte.name})>"
