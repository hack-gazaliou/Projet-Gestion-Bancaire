from enum import IntEnum
from Modele.SQL.SQLComptes import SQLCompte
import logging

logger = logging.getLogger(__name__)


class TypeCompte(IntEnum):
    COURANT = 0
    LIVRET_A = 1
    PEL = 2


class Compte:
    def __init__(
        self, id: int, type_compte: TypeCompte, id_client: int, initial_amount: int = 0
    ) -> None:
        self._type_compte = type_compte
        self._id_client = id_client
        self._id = id
        # On ne crée en base QUE si l'id n'existe pas encore
        if self._id is None:
            # Note : Assurez-vous que SQLCompte.creer accepte un montant initial
            new = SQLCompte.creer(self._type_compte, self._id_client, initial_amount)
            self._id = new.id

    @property
    def solde(self) -> int:
        """Calcule le solde actuel en sommant toutes les opérations."""
        total_credits, total_debits = SQLCompte.get_credits_and_debits(self._id)
        return total_credits - total_debits

    @classmethod
    def load(cls, account_id):
        """
        Load an account based on his id
        """
        account = SQLCompte.get(account_id)
        if not account:
            logger.error(f"Account not found")
            return None
        loaded_account = cls(id=account.id, type_compte=account.type_compte, id_client=account.id_client)  # type: ignore

    def __repr__(self):
        return f"<Compte(id={self._id}, type={self._type_compte.name}, solde={self.solde}€)>"
