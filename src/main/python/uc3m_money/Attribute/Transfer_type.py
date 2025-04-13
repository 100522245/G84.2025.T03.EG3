from uc3m_money.Attribute.Attribute import Attribute

class Transfer_type(Attribute):
    def __init__(self, attr_value):
        self._error_message = "Invalid transfer type"
        self._validation_pattern = (r"(ORDINARY|INMEDIATE|URGENT)")
        self._attr_value = self._validate(attr_value)