"""Importaciones"""
# pylint: disable = [invalid-name]
from uc3m_money.data.Attribute.Attribute import Attribute


class Transfer_type(Attribute):
    """Clase Transfer_type(Attribute)"""
    # pylint: disable = [too-few-public-methods]
    def __init__(self, attr_value):
        super().__init__()
        self._error_message = "Invalid transfer type"
        self._validation_pattern = r"(ORDINARY|INMEDIATE|URGENT)"
        self._attr_value = self._validate(attr_value)
