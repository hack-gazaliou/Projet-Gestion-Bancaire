"""
Unitary test for the Operation class and associated method
"""

from unittest.mock import patch, MagicMock
from datetime import datetime
import pytest
from Modele.operation import Operation, OperationException


class TestOperation:
    """
    Test operation class
    """

    @patch("Modele.operation.SQLOperation.execute_transfer")
    def test_execute_success(self, mock_transfer):
        """Test a normal transaction (with success)"""
        fixed_date = datetime(2024, 1, 1, 12, 0)
        mock_op_sql = MagicMock()
        mock_op_sql.get_id.return_value = 123
        mock_op_sql.date_operation = fixed_date
        mock_transfer.return_value = mock_op_sql

        op = Operation(id_source_account=1, id_target_account=2, amount=50)
        op.execute()

        assert op.get_id() == 123  # type: ignore
        assert op.date_operation == fixed_date  # type: ignore
        mock_transfer.assert_called_once_with(1, 2, 50)

    @patch("Modele.operation.SQLOperation.execute_transfer")
    def test_execute_failed(self, mock_transfer):
        """Test the OperationException raise when the transaction fail"""
        mock_transfer.return_value = None

        op = Operation(id_source_account=1, id_target_account=999, amount=50)

        with pytest.raises(OperationException):
            op.execute()

    @patch("Modele.operation.SQLOperation.get_by_account")
    def test_get_account_history(self, mock_get_sql):
        """Test the recovery of the transaction history"""
        mock_op1 = MagicMock()
        mock_op1.id = 101
        mock_op1.id_compte_source = 1
        mock_op1.id_compte_cible = 2
        mock_op1.montant = 100
        mock_op1.date_operation = datetime(2024, 1, 1)

        mock_op2 = MagicMock()
        mock_op2.id = 102
        mock_op2.id_compte_source = 3
        mock_op2.id_compte_cible = 1
        mock_op2.montant = 50
        mock_op2.date_operation = datetime(2024, 1, 2)

        mock_get_sql.return_value = [mock_op1, mock_op2]

        history = Operation.get_account_history(1)

        assert len(history) == 2
        assert history[0].get_id() == 101  # type: ignore
        assert history[0].amount == 100
        assert history[1].id_target_account == 1
        mock_get_sql.assert_called_once_with(1)
