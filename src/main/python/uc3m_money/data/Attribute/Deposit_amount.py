"""Importaciones"""
# pylint: disable = [invalid-name]
# pylint: disable = [relative-beyond-top-level]
from uc3m_money.account_management_exception import AccountManagementException
from .Attribute import Attribute

# pylint: disable = [invalid-name]
class Deposit_amount(Attribute):
    """Clase Deposit_amount(Attribute)"""
    # pylint: disable = [too-few-public-methods]
    def __init__(self, attr_value):
        super().__init__()
        self._error_message = "Error - Invalid deposit amount"
        self._validation_pattern = r"^EUR [0-9]{4}\.[0-9]{2}"
        self._attr_value = self._validate(attr_value)

    def _validate(self, value):
        value = str(value)
        value = super()._validate(value)
        amount = value

        deposit_amount = float(amount[4:])
        if deposit_amount == 0:
            raise AccountManagementException(
                "Error - Deposit must be greater than 0")

        return value
