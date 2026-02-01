"""
SQL Operations Management Module.
Defines the data model for transactions between accounts.
"""

import logging
from datetime import datetime

from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime

from Modele.SQL.sql_manager import Base, SESSIONLOCAL

logger = logging.getLogger(__name__)


class SQLOperation(Base):
    """
    Represents a banking operation between two accounts in the database.
    """

    __tablename__ = "operations"
    id = Column(Integer, primary_key=True, autoincrement=True)

    id_compte_source = Column(Integer, ForeignKey("comptes.id"), nullable=False)
    id_compte_cible = Column(Integer, ForeignKey("comptes.id"), nullable=False)
    montant = Column(Float, nullable=False)
    date_operation = Column(DateTime, default=datetime.now)

    def get_id(self):
        """Returns the operation unique identifier."""
        return self.id

    @classmethod
    def execute_transfer(cls, source_id, target_id, amount):
        """
        Creates a transaction in the database and executes it.
        """
        with SESSIONLOCAL() as session:
            # pylint: disable=import-outside-toplevel
            from Modele.SQL.sql_comptes import SQLCompte

            source = session.query(SQLCompte).get(source_id)
            cible = session.query(SQLCompte).get(target_id)

            if not source or not cible:
                logger.error("Transfer error: One of the accounts does not exist.")
                return None

            nouvelle_operation = cls(
                id_compte_source=source_id, id_compte_cible=target_id, montant=amount
            )

            session.add(nouvelle_operation)
            session.commit()

            logger.debug(
                "Transfer of %s€ successful from %s to %s.",
                amount,
                source_id,
                target_id,
            )
            return nouvelle_operation

    @classmethod
    def get_by_account(cls, account_id: int):
        """
        Retrieves all transactions associated with a specific account.
        """
        with SESSIONLOCAL() as session:
            return (
                session.query(cls)
                .filter(
                    (cls.id_compte_source == account_id)
                    | (cls.id_compte_cible == account_id)
                )
                .order_by(cls.date_operation.desc())
                .all()
            )

    def __repr__(self):
        return (
            f"<Operation(id={self.id}, from={self.id_compte_source} "
            f"to={self.id_compte_cible}, amount={self.montant}€)>"
        )
