from .Attribute import Attribute
from uc3m_money.account_management_exception import AccountManagementException

class Transfer_amount(Attribute):
    def __init__(self, attr_value):
        self._error_message = "Invalid transfer amount"
        self._validation_pattern = r"^EUR [0-9]{4}\.[0-9]{2}"
        self._attr_value = self._validate(attr_value)

    def _validate_transfer_amount(self, attr_value:str)->str:
        """method for validating an amount"""
        attr_value = super()._validate(attr_value)
        amount = attr_value

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

        return attr_value