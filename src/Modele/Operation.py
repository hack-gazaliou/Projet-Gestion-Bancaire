from datetime import datetime
from Modele.SQL.SQLComptes import SQLCompte
from Modele.SQL.SQLOperations import SQLOperation
import logging

logger = logging.getLogger(__name__)


class Operation:
    def __init__(
        self, id_source_account: int, id_target_account: int, amount: int
    ) -> None:
        self.id_source_account = id_source_account
        self.id_target_account = id_target_account
        self.amount = amount
        self.date_operation = datetime.now()
        self.id = 0

    def execute(self) -> None:
        """
        Execute the operation
        """
        operation = SQLOperation.execute_transfer(
            self.id_source_account, self.id_target_account, self.amount
        )
        if operation is not None:
            self.id = operation.get_id()
            self.date_operation = operation.date_operation  # sync the 2 objects
        else:
            logger.error("The transfert wasn't committed, please retry")
            raise OperationException

    def __repr__(self):
        return f"<Operation(id={self.id}, from={self.id_source_account} to={self.id_target_account}, amount={self.amount}€)>"


class OperationException(Exception):
    def __repr__(self) -> str:
        return "The operation couldn't be committed to the database please retry"
