from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime
from Modele.SQLManager import Base, SessionLocal
from datetime import datetime

class Operation(Base):
    __tablename__ = 'operations'

    id = Column(Integer, primary_key=True, autoincrement=True)
    # On lie à l'ID de la table 'comptes'
    id_compte_source = Column(Integer, ForeignKey('comptes.id'), nullable=False)
    id_compte_cible = Column(Integer, ForeignKey('comptes.id'), nullable=False)
    montant = Column(Float, nullable=False)
    date_operation = Column(DateTime, default=datetime.now)

    @classmethod
    def transferer(cls, source_id, cible_id, montant):
        """
        Crée une opération et met à jour les soldes des deux comptes.
        """
        with SessionLocal() as session:
            from Modele.Compte import Compte # Import local pour éviter les imports circulaires
            
            source = session.query(Compte).get(source_id)
            cible = session.query(Compte).get(cible_id)

            if not source or not cible:
                print("Erreur : L'un des comptes n'existe pas.")
                return None

            # Si montant > 0 : source donne à cible
            #source.solde -= montant
            #cible.solde += montant

            nouvelle_op = cls(
                id_compte_source=source_id,
                id_compte_cible=cible_id,
                montant=montant
            )
            
            session.add(nouvelle_op)
            session.commit()
            print(f"Transfert de {montant}€ réussi de {source_id} vers {cible_id}.")
            return nouvelle_op

    def __repr__(self):
        return f"<Operation(id={self.id}, de={self.id_compte_source} vers={self.id_compte_cible}, montant={self.montant}€)>"