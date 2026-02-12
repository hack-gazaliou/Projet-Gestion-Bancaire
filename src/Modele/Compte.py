"""
Account Management Module.
Handles controller to database link for accounts.
"""

import logging

from Modele.SQL.sql_comptes import SQLCompte
from Modele.type_compte import TypeCompte


logger = logging.getLogger(__name__)


class Compte:
    """
    Represents a bank account.
    """

    def __init__(
        self,
        account_id: int | None,
        type_compte: TypeCompte,
        id_client: int,
        initial_amount: int = 0,
    ) -> None:
        self._type_compte = type_compte
        self._id_client = id_client
        self._id = account_id
        # On ne crée en base QUE si l'id n'existe pas encore
        if self._id is None:
            # Note : Assurez-vous que SQLCompte.creer accepte un montant initial
            new = SQLCompte.creer(self._type_compte, self._id_client, initial_amount)
            self._id = new.id

    def get_id(self):
        """Get the the id"""
        return self._id

    def get_type_compte(self):
        """Get the account type"""
        return self._type_compte

    @property
    def solde(self) -> int:
        """Calcule le solde actuel en sommant toutes les opérations."""
        total_credits, total_debits = SQLCompte.get_credits_and_debits(self._id)  # type: ignore
        return total_credits - total_debits

    @classmethod
    def load(cls, account_id):
        """
        Load an account based on his id
        """
        account = SQLCompte.get(account_id)
        if not account:
            logger.error("Account not found")
            return None
        loaded_account = cls(
            account_id=account.id,  # type: ignore
            type_compte=account.type_compte,  # type: ignore
            id_client=account.id_client,  # type: ignore
        )
        return loaded_account

    def __repr__(self):
        return f"<Compte(id={self._id}, type={self._type_compte.name})>"  # noqa: E501
