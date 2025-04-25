"""Importaciones"""
# pylint: disable = [invalid-name]
import re
from uc3m_money.account_management_exception import AccountManagementException

# pylint: disable = [too-few-public-methods]
class Attribute:
    """Clase Attribute"""
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
        """Property value"""
        return self._attr_value

    @value.setter
    def value(self, attr_value):
        self._attr_value = attr_value
