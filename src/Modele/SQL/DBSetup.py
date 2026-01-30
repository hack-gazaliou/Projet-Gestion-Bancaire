from Modele.SQL.SQLManager import engine, Base, SessionLocal
from Modele.Compte import Compte, TypeCompte
import logging

logger = logging.getLogger(__name__)


def initialiser_bdd() -> None:
    """
    Initialise la base de données SQL
    """
    Base.metadata.drop_all(bind=engine)
    logger.debug("Database emptied")
    Base.metadata.create_all(bind=engine)
    logger.info("Database Initialized")


def initialiser_coffre_fort() -> None:
    """
    Initialise le compte 0 pour permettre de créditer un compte lors de sa création
    """
    with SessionLocal() as session:
        coffre = session.query(Compte).filter_by(id=0).first()

        if not coffre:
            coffre = Compte(id=0, type_compte=TypeCompte.COURANT)  # id 0
            session.add(coffre)
            try:
                session.commit()
                logger.info("The safe was initialized")
            except Exception:
                session.rollback()
                logger.error(
                    "Failed to initialize the safe, ID 0 may be reserved, check your configuration..."
                )
