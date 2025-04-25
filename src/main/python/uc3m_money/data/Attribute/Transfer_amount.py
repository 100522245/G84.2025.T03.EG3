"""Importaciones"""
# pylint: disable = [invalid-name]
# pylint: disable = [relative-beyond-top-level]
from uc3m_money.account_management_exception import AccountManagementException
from .Attribute import Attribute


class Transfer_amount(Attribute):
    """Clase Transfer_amount(Attribute)"""
    # pylint: disable = [too-few-public-methods]
    def __init__(self, attr_value):
        super().__init__()
        self._error_message = "Invalid transfer amount"
        self._validation_pattern = r""
        self._attr_value = self._validate(attr_value)

    def _validate(self, value:str)->str:
        """method for validating an amount"""
        amount = value

        try:
            transfer_amount  = float(amount)
        except ValueError as value_error:
            raise AccountManagementException("Invalid transfer amount") from value_error

        if '.' in str(transfer_amount) and len(
                str(transfer_amount).split('.')[1]) > 2:
            raise AccountManagementException(
                "Invalid transfer amount")

        if transfer_amount < 10 or transfer_amount > 10000:
            raise AccountManagementException("Invalid transfer amount")

        return value
