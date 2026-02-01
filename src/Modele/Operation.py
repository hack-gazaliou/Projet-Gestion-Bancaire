"""
Operations Management Module.
Defines the data model for transactions between accounts.
"""
import logging
from datetime import datetime
from Modele.SQL.sql_operations import SQLOperation

logger = logging.getLogger(__name__)


class Operation:
    """
    Represent operations
    """
    def __init__(
        self, id_source_account: int, id_target_account: int, amount: int
    ) -> None:
        self.id_source_account = id_source_account
        self.id_target_account = id_target_account
        self.amount = amount
        self.date_operation = datetime.now()
        self._id = 0

    def execute(self) -> None:
        """
        Execute the operation
        """
        operation = SQLOperation.execute_transfer(
            self.id_source_account, self.id_target_account, self.amount
        )
        if operation is not None:
            self._id = operation.get_id()
            self.date_operation = operation.date_operation  # sync the 2 objects
        else:
            logger.error("The transfert wasn't committed, please retry")
            raise OperationException
    def get_id(self):
        """
        return the id of the operation
        """
        return self._id
    def set_id(self, new_id):
        """
        Set a new id to the operation (for test only)
        """
        self._id = new_id
    @classmethod
    def get_account_history(cls, account_id: int) -> list['Operation']:
        """Gives all the transactions associated with an account"""
        sql_ops = SQLOperation.get_by_account(account_id)
        history = []
        for sql_op in sql_ops:
            op = cls(
                id_source_account=sql_op.id_compte_source, #type: ignore
                id_target_account=sql_op.id_compte_cible, #type: ignore
                amount=sql_op.montant #type: ignore
            )
            op._id = sql_op.id
            op.date_operation = sql_op.date_operation
            history.append(op)
        return history
    def __repr__(self):
        return f"""<Operation(id={self._id},
                from={self.id_source_account}
                to={self.id_target_account},
                amount={self.amount}€)>""" # noqa : E501


class OperationException(Exception):
    """
    Operation Exception class to handle error specific to this module
    """
    def __repr__(self) -> str:
        return "The operation couldn't be committed to the database please retry"
