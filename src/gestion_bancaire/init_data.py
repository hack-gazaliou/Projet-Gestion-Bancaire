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
            "DUPONT",
            "Jean",
            "j.dupont@email.fr",
            "0612345678",
            "12 rue des Lilas, 75011 Paris",
            [("COURANT", 2450.50), ("LIVRET_A", 12000.00)],
        ),
        (
            "MARTIN",
            "Alice",
            "alice.martin@gmail.com",
            "0623456789",
            "45 avenue de la République, 69002 Lyon",
            [("COURANT", 150.00), ("LIVRET_A", 450.00)],
        ),
        (
            "LEFEBVRE",
            "Thomas",
            "t.lefebvre@outlook.fr",
            "0734567890",
            "8 bis rue de la Paix, 33000 Bordeaux",
            [("COURANT", 4200.00), ("PEL", 15000.00), ("LIVRET_A", 22950.00)],
        ),
        (
            "MOREAU",
            "Camille",
            "c.moreau@wanadoo.fr",
            "0645678901",
            "22 place de la Mairie, 44000 Nantes",
            [("COURANT", 890.30)],
        ),
        (
            "PETIT",
            "Lucas",
            "lucas.petit@etudiant.univ.fr",
            "0656789012",
            "Résidence Universitaire, Chambre 402, 31000 Toulouse",
            [("COURANT", 12.45), ("LIVRET_A", 100.00)],
        ),
        (
            "ROUX",
            "Isabelle",
            "isabelle.roux@orange.fr",
            "0667890123",
            "5 villa des Roses, 59000 Lille",
            [("COURANT", 3100.00), ("PEL", 45000.00)],
        ),
        (
            "GARCIA",
            "Antoine",
            "a.garcia@free.fr",
            "0778901234",
            "102 boulevard Perrier, 13008 Marseille",
            [("COURANT", -120.00), ("LIVRET_A", 50.00)], # Cas d'un compte à découvert
        ),
        (
            "BERNARD",
            "Marie",
            "m.bernard@club-internet.fr",
            "0689012345",
            "3 route de la Corniche, 06000 Nice",
            [("COURANT", 12500.00), ("LIVRET_A", 22950.00), ("PEL", 61200.00)],
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
