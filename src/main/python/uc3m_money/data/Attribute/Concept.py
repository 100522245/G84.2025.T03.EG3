"""Importaciones"""
# pylint: disable = [invalid-name]
from uc3m_money.data.Attribute.Attribute import Attribute


class Concept(Attribute):
    """Clase Concept(Attribute)"""
    # pylint: disable = [too-few-public-methods]
    def __init__(self, attr_value):
        # pylint: disable = [super-init-not-called]
        super().__init__()
        self._error_message = "Invalid concept format"
        self._validation_pattern = (r"^(?=^.{10,30}$)([a-zA-Z]+(\s["
                                     r"a-zA-Z]+)+)$")
        self._attr_value = self._validate(attr_value)
