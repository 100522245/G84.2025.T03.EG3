from .Attribute import Attribute
from uc3m_money.account_management_exception import AccountManagementException

class IBAN(Attribute):
    def __init__(self, attr_value):
        self._error_message = "Invalid IBAN format"
        self._validation_pattern = r"^ES[0-9]{22}"
        self._attr_value = self._validate(attr_value)

    def _validate_iban(self, attr_value:str)->str:
        """method for validating an iban"""
        attr_value = super()._validate(attr_value)
        iban = attr_value

        digitos_control = iban[2:4]
        # replacing the control
        parte_numerica_iban = iban[:2] + "00" + iban[4:]
        iban_reordenado = parte_numerica_iban[4:] + parte_numerica_iban[:4]

        # Convertir el IBAN en una cadena numérica, reemplazando letras por números
        parte_numerica_iban = (
            iban_reordenado.replace('A', '10').replace('B', '11').
            replace('C', '12').replace('D', '13').replace('E', '14').
            replace('F', '15').replace('G', '16').replace('H', '17').
            replace('I', '18').replace('J', '19').replace('K', '20').
            replace('L', '21').replace('M', '22').replace('N', '23').
            replace('O', '24').replace('P', '25').replace('Q', '26').
            replace('R', '27').replace('S', '28').replace('T', '29').replace(
                'U', '30').
            replace('V', '31').replace('W', '32').replace('X',
                                                          '33').replace('Y',
                                                                        '34').replace(
                'Z', '35'))

        # Mover los cuatro primeros caracteres al final

        # Convertir la cadena en un número entero
        iban_integer = int(parte_numerica_iban)

        # Calcular el módulo 97
        mod_resultado = iban_integer % 97

        # Calcular el dígito de control (97 menos el módulo)
        digitos_control_esperados = 98 - mod_resultado

        if int(digitos_control) != digitos_control_esperados:
            # print(digitos_control_esperados)
            raise AccountManagementException("Invalid IBAN control digit")

        return attr_value

