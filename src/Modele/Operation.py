from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime
from Modele.SQLManager import Base, SessionLocal
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class Operation(Base):

    __tablename__ = 'operations'
    id = Column(Integer, primary_key=True, autoincrement=True)

    id_compte_source = Column(Integer, ForeignKey('comptes.id'), nullable=False)
    id_compte_cible = Column(Integer, ForeignKey('comptes.id'), nullable=False)
    montant = Column(Float, nullable=False)
    date_operation = Column(DateTime, default=datetime.now)

    @classmethod
    def transferer(cls, source_id, target_id, amount):
        """
        Crée une opération et met à jour les soldes des deux comptes.
        """
        with SessionLocal() as session:
            from Modele.Compte import Compte # import local pour éviter les imports circulaires
            
            source = session.query(Compte).get(source_id)
            cible = session.query(Compte).get(target_id)

            if not source or not cible:
                logger.error("Transfer error: One of the accounts does not exist.")
                return None

            nouvelle_operation = cls(
                id_compte_source=source_id,
                id_compte_cible=target_id,
                montant=amount
            )
            
            session.add(nouvelle_operation)
            session.commit()
            logger.debug(f"Transfer of {amount}€ successfully completed from {source_id} to {target_id}.")
            return nouvelle_operation

    def __repr__(self):
        return f"<Operation(id={self.id}, de={self.id_compte_source} vers={self.id_compte_cible}, montant={self.montant}€)>"