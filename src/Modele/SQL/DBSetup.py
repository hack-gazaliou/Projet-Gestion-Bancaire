import logging

from Modele.SQL.sql_comptes import (
    SQLCompte,
)
from Modele.SQL.sql_manager import Base, SessionLocal, engine
from Modele.SQL.sql_operations import SQLOperation
from Modele.SQL.SQLCustomer import Customer
from Modele.type_compte import TypeCompte

logger = logging.getLogger(__name__)


def initialiser_bdd() -> None:
    """
    Vide et recrée la base de données SQL.
    """
    logger.info("Dropping all tables...")
    Base.metadata.drop_all(bind=engine)
    logger.debug("Database emptied")

    logger.info("Creating all tables...")
    Base.metadata.create_all(bind=engine)
    logger.info("Database Initialized")


def initialiser_coffre_fort() -> None:
    """
    Initialise le Client 0 (System) et le Compte 0 (Coffre)
    """
    with SessionLocal() as session:
        try:
            # CRÉATION DU CLIENT 0
            client_zero = session.query(Customer).filter_by(customer_id=0).first()
            if not client_zero:
                logger.info("Creating System Client (ID 0)...")
                client_zero = Customer(
                    customer_id=0,
                    first_name="SYSTEM",
                    last_name="BANK",
                    phone="0000",
                    email="root@localhost",
                    card_number="0000",
                    address="Server",
                )
                session.add(client_zero)
                session.commit()

            # CRÉATION DU COMPTE 0
            coffre = session.query(SQLCompte).filter_by(id=0).first()
            if not coffre:
                logger.info("Creating Safe Account (ID 0)...")
                coffre = SQLCompte(id=0, type_compte=TypeCompte.COURANT, id_client=0)
                session.add(coffre)

                op_init = SQLOperation(
                    id_compte_source=0, id_compte_cible=0, montant=10000000000000.0
                )
                session.add(op_init)

                session.commit()
                logger.info("The safe was initialized with funds.")
            else:
                logger.info("Safe already exists.")

        except Exception as e:
            session.rollback()
            logger.error(f"Failed to initialize the safe: {e}")
