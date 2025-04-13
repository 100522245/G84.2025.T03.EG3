import re
from uc3m_money.account_management_exception import AccountManagementException

class Attribute():
    def __init__(self):
        self._attr_value = ""
        self._error_message = ""
        self._validation_pattern = r""

    def _validate(self, value):
        formato = re.compile(self._validation_pattern)
        formato_fullmatch = formato.fullmatch(value)
        if not formato_fullmatch:
            raise AccountManagementException(self._error_message)
        return value

    @property
    def value(self):
        return self._attr_value

    @value.setter
    def value(self, attr_value):
        self._attr_value = attr_value