from .Attribute import Attribute
from uc3m_money.account_management_exception import AccountManagementException
from uc3m_money.Attribute.Transfer_amount import Transfer_amount

class Deposit_amount(Attribute):
    def __init__(self, attr_value):
        self._error_message = "Error - Invalid deposit amount"
        self._validation_pattern = r"^EUR [0-9]{4}\.[0-9]{2}"
        self._attr_value = self._validate(attr_value)

    def _validate(self, attr_value):
        attr_value = str(attr_value)
        attr_value = super()._validate(attr_value)
        amount = attr_value

        deposit_amount = float(amount[4:])
        if deposit_amount == 0:
            raise AccountManagementException(
                "Error - Deposit must be greater than 0")

        return attr_value