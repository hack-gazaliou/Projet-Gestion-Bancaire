from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime
from Modele.SQL.SQLManager import Base, SessionLocal
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class SQLOperation(Base):
    __tablename__ = "operations"
    id = Column(Integer, primary_key=True, autoincrement=True)

    id_compte_source = Column(Integer, ForeignKey("comptes.id"), nullable=False)
    id_compte_cible = Column(Integer, ForeignKey("comptes.id"), nullable=False)
    montant = Column(Float, nullable=False)
    date_operation = Column(DateTime, default=datetime.now)

    def get_id(self):
        return self.id

    @classmethod
    def execute_transfer(cls, source_id, target_id, amount):
        """
        Create a transaction in the database and execute it
        """
        with SessionLocal() as session:
            from Modele.SQL.SQLComptes import (
                SQLCompte,
            )  # import local pour éviter les imports circulaires

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
                f"Transfer of {amount}€ successfully completed from {source_id} to {target_id}." # noqa: E501
            )
            return nouvelle_operation

    @classmethod
    def get_by_account(cls, account_id: int):
        """Gives all transactions associated with an account"""
        with SessionLocal() as session:
            return session.query(cls).filter(
                (cls.id_compte_source == account_id) | 
                (cls.id_compte_cible == account_id)
            ).order_by(cls.date_operation.desc()).all()
        
    def __repr__(self):
        return f"<Operation(id={self.id}, de={self.id_compte_source} vers={self.id_compte_cible}, montant={self.montant}€)>"# noqa: E501
