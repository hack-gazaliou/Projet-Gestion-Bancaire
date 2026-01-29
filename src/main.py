import logging
import Controleur.Logger
from Modele.DBSetup import initialiser_bdd, initialiser_coffre_fort
from Modele.Compte import Compte, TypeCompte
from Modele.Operation import Operation

logger = logging.getLogger(__name__)

def main():
    initialiser_bdd()
    initialiser_coffre_fort()

    c1 = Compte.creer(TypeCompte.COURANT, 1000.0)
    c2 = Compte.creer(TypeCompte.COURANT, 10000.0)
    # On fait un transfert
    Operation.transferer(source_id=c1.id, target_id=c2.id, amount=200.0)

    # L'accès à solde déclenche le calcul (1000 - 200)
    logger.debug(f"Solde compte 1 : {c1.solde}€")
    logger.debug(f"Solde compte 2 : {c2.solde}€")
    logger.info("Application stop")


if __name__ == "__main__":
    main()