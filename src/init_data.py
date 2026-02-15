import logging
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("InitDB")

from Controleur.controleur import Controller  # noqa: E402
from Modele.SQL.db_setup import initialiser_bdd, initialiser_coffre_fort  # noqa: E402


def init_db():
    logger.info("==========================================")
    logger.info("   INITIALISATION DE LA BASE DE DONNEES   ")
    logger.info("==========================================")

    # 1. Remise à zéro
    initialiser_bdd()
    initialiser_coffre_fort()

    controller = Controller()

    logger.info("Generating Mock Clients...")

    liste_clients = [
        (
            "BOND",
            "James",
            "007@mi6.uk",
            "0600700700",
            "Londres, UK",
            [("COURANT", 1000.00), ("LIVRET_A", 25000.00)],
        ),
        (
            "WAYNE",
            "Bruce",
            "batman@gotham.city",
            "0102030405",
            "Manoir Wayne, Gotham",
            [("COURANT", 10000000.00), ("PEL", 60000.00)],
        ),
        (
            "POTTER",
            "Harry",
            "hpotter@poudlard.uk",
            "0666666666",
            "4 Privet Drive, Placard sous l'escalier",
            [("COURANT", 50.00)],
        ),
        (
            "STARK",
            "Tony",
            "ironman@avengers.com",
            "0777888999",
            "Stark Tower, New York",
            [("COURANT", 50000000.50), ("LIVRET_A", 22950.00), ("PEL", 61200.00)],
        ),
        (
            "SIMPSON",
            "Homer",
            "homer@springfield.nuc",
            "0612345678",
            "742 Evergreen Terrace",
            [("COURANT", 15.50), ("LIVRET_A", 10.00)],
        ),
        (
            "WHITE",
            "Walter",
            "heisenberg@lospollos.com",
            "0699887766",
            "Albuquerque, New Mexico",
            [("COURANT", 500.00), ("LIVRET_A", 850000.00)],
        ),
        (
            "CROFT",
            "Lara",
            "lara@tombraid.er",
            "0655443322",
            "Croft Manor, Surrey",
            [("COURANT", 25000.00)],
        ),
        (
            "KENOBI",
            "Obi-Wan",
            "hello.there@jedi.council",
            "0600000001",
            "Tatooine, Dune Sea",
            [("COURANT", 0.00)],
        ),
    ]

    count_clients = 0

    for nom, prenom, email, tel, adr, comptes in liste_clients:
        succes, msg = controller.creer_nouveau_client(nom, prenom, email, tel, adr)

        if succes:
            clients = controller.get_tous_les_clients()

            new_id = clients[-1]["id"]

            logger.info(f"Client created: {prenom} {nom} (ID: {new_id})")
            count_clients += 1

            for type_cpt, solde in comptes:
                succes_cpt, msg_cpt = controller.ajouter_compte_client(
                    new_id, type_cpt, solde
                )
                if succes_cpt:
                    logger.info(f"    ├─ Account {type_cpt} added with {solde} €")
                else:
                    logger.error(f"    └─ Error adding account {type_cpt}: {msg_cpt}")
        else:
            logger.warning(f" Failed to create {nom}: {msg}")

    logger.info(f"--- INITIALIZATION COMPLETE ({count_clients} clients created) ---")


if __name__ == "__main__":
    init_db()
