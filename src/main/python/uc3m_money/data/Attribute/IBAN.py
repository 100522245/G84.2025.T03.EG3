"""Importaciones"""
# pylint: disable = [invalid-name]
# pylint: disable = [relative-beyond-top-level]
from uc3m_money.account_management_exception import AccountManagementException
from .Attribute import Attribute


class IBAN(Attribute):
    """Clase IBAN(Attribute)"""
    # pylint: disable = [too-few-public-methods]
    def __init__(self, attr_value):
        super().__init__()
        self._error_message = "Invalid IBAN format"
        self._validation_pattern = r"^ES[0-9]{22}"
        self._attr_value = self._validate(attr_value)

    def _validate(self, value: str) -> str:
        """method for validating an iban"""
        value = super()._validate(value)
        iban = value

        digitos_control = iban[2:4]
        parte_numerica_iban = iban[:2] + "00" + iban[4:]
        iban_reordenado = parte_numerica_iban[4:] + parte_numerica_iban[:4]

        parte_numerica_iban = (
            iban_reordenado.replace('A', '10').replace('B', '11').
            replace('C', '12').replace('D', '13').replace('E', '14').
            replace('F', '15').replace('G', '16').replace('H', '17').
            replace('I', '18').replace('J', '19').replace('K', '20').
            replace('L', '21').replace('M', '22').replace('N', '23').
            replace('O', '24').replace('P', '25').replace('Q', '26').
            replace('R', '27').replace('S', '28').replace('T', '29').
            replace('U', '30').replace('V', '31').replace('W', '32').
            replace('X', '33').replace('Y', '34').replace('Z', '35'))

        iban_integer = int(parte_numerica_iban)
        mod_resultado = iban_integer % 97
        digitos_control_esperados = 98 - mod_resultado

        if int(digitos_control) != digitos_control_esperados:
            raise AccountManagementException("Invalid IBAN control digit")

        return value
