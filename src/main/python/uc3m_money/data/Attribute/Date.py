from datetime import datetime, timezone
from uc3m_money.data.Attribute.Attribute import Attribute
from uc3m_money.account_management_exception import AccountManagementException

class Date(Attribute):
    def __init__(self, attr_value):
        self._error_message = "Invalid date format"
        self._validation_pattern = (r"^(([0-2]\d|3[0-1])\/(0\d|1["
                                r"0-2])\/\d\d\d\d)$")
        self._attr_value = self._validate(attr_value)

    def _validate(self, attr_value):
        attr_value = super()._validate(attr_value)

        transfer_date = attr_value
        try:
            fecha_convertida = datetime.strptime(transfer_date, "%d/%m/%Y").date()
        except ValueError as value_error:
            raise AccountManagementException("Invalid date format") from (
                value_error)

        fecha_actual = datetime.now(timezone.utc).date()
        if fecha_convertida < fecha_actual:
            raise AccountManagementException("Transfer date must be today or later.")

        if fecha_convertida.year < 2025 or fecha_convertida.year > 2050:
            raise AccountManagementException("Invalid date format")

        return attr_value