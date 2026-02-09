"""
Database Initialization Module.
Provides functions to set up the database schema and initial state.
"""

import logging

from sqlalchemy.exc import SQLAlchemyError

from Modele.Compte import Compte
from Modele.type_compte import TypeCompte
from Modele.SQL.sql_manager import SESSIONLOCAL, Base, engine

logger = logging.getLogger(__name__)


def initialiser_bdd() -> None:
    """
    Drops all existing tables and recreates the database schema from scratch.
    """
    Base.metadata.drop_all(bind=engine)
    logger.debug("Database emptied")
    Base.metadata.create_all(bind=engine)
    logger.info("Database Initialized")


def initialiser_coffre_fort() -> None:
    """
    Initializes the bank's master account (ID 0) if it does not already exist.
    """
    with SESSIONLOCAL() as session:
        coffre = session.query(Compte).filter_by(id=0).first()

        if not coffre:
            # Create the master account (The Safe) with ID 0
            coffre = Compte(account_id=0, type_compte=TypeCompte.COURANT, id_client=0)
            session.add(coffre)
            try:
                session.commit()
                logger.info("The safe was initialized")
            except SQLAlchemyError as e:
                session.rollback()
                logger.error(
                    "Failed to initialize the safe. "
                    "ID 0 may be reserved or there is a constraint conflict: %s",
                    e,
                )
