"""Account manager module """
import re
import json
from datetime import datetime, timezone
from uc3m_money.account_management_exception import AccountManagementException
from uc3m_money.account_management_config import (TRANSFERS_STORE_FILE,
                                        DEPOSITS_STORE_FILE,
                                        TRANSACTIONS_STORE_FILE,
                                        BALANCES_STORE_FILE)

from uc3m_money.transfer_request import TransferRequest
from uc3m_money.account_deposit import AccountDeposit


class AccountManager:
    """Class for providing the methods for managing the orders"""
    def __init__(self):
        pass

    @staticmethod
    def validate_iban(iban: str):
        """
    Calcula el dígito de control de un IBAN español.

    Args:
        iban (str): El IBAN sin los dos últimos dígitos (dígito de control).

    Returns:
        str: El dígito de control calculado.
        """
        formato_iban = re.compile(r"^ES[0-9]{22}")
        if not formato_iban.fullmatch(iban):
            raise AccountManagementException("Invalid IBAN format")

        digitos_control = iban[2:4]
        #replacing the control
        parte_numerica_iban = iban[:2] + "00" + iban[4:]
        iban_reordenado = parte_numerica_iban[4:] + parte_numerica_iban[:4]


        # Convertir el IBAN en una cadena numérica, reemplazando letras por números
        parte_numerica_iban = (iban_reordenado.replace('A', '10').replace('B', '11').
                replace('C', '12').replace('D', '13').replace('E', '14').
                replace('F', '15').replace('G', '16').replace('H', '17').
                replace('I', '18').replace('J', '19').replace('K', '20').
                replace('L', '21').replace('M', '22').replace('N', '23').
                replace('O', '24').replace('P', '25').replace('Q', '26').
                replace('R', '27').replace('S', '28').replace('T', '29').replace('U', '30').
                replace('V', '31').replace('W', '32').replace('X',
                                                              '33').replace('Y', '34').replace('Z', '35'))

        # Mover los cuatro primeros caracteres al final

        # Convertir la cadena en un número entero
        iban_integer = int(iban)

        # Calcular el módulo 97
        mod_resultado = iban_integer % 97

        # Calcular el dígito de control (97 menos el módulo)
        digitos_control_esperados = 98 - mod_resultado

        if int(digitos_control) != digitos_control_esperados:
            #print(digitos_control_esperados)
            raise AccountManagementException("Invalid IBAN control digit")

        return iban


    def validate_concept(self, concept: str):
        """regular expression for checking the minimum and maximum length as well as
        the allowed characters and spaces restrictions
        there are other ways to check this"""
        formato_concept = re.compile(r"^(?=^.{10,30}$)([a-zA-Z]+(\s["
                                   r"a-zA-Z]+)+)$")
        if not formato_concept.fullmatch(concept):
            raise AccountManagementException ("Invalid concept format")


    def validate_transfer_date(self, transfer_date):
        """validates the arrival date format  using regex"""
        formato_transfer_date = re.compile(r"^(([0-2]\d|3[0-1])\/(0\d|1["
                                r"0-2])\/\d\d\d\d)$")
        if not formato_transfer_date.fullmatch(transfer_date):
            raise AccountManagementException("Invalid date format")

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
        return transfer_date


    #pylint: disable=too-many-arguments
    def create_transfer_request(self, from_iban: str,
                                to_iban: str,
                                concept: str,
                                transfer_type: str,
                                transfer_date: str,
                                amount: float)->str:
        """first method: receives transfer info and
        stores it into a file"""
        self.validate_iban(from_iban)
        self.validate_iban(to_iban)
        self.validate_concept(concept)

        if not re.fullmatch(r"(ORDINARY|INMEDIATE|URGENT)", transfer_type):
            raise AccountManagementException("Invalid transfer type")

        self.validate_transfer_date(transfer_date)

        try:
            transfer_amount  = float(amount)
        except ValueError as value_error:
            raise AccountManagementException("Invalid transfer amount") from value_error

        if '.' in str(transfer_amount) and len(
                str(transfer_amount).split('.')[1]) > 2:
            raise AccountManagementException(
                "Invalid transfer amount precision")

        if transfer_amount < 10 or transfer_amount > 10000:
            raise AccountManagementException("Invalid transfer amount")

        new_tranfer = TransferRequest(from_iban=from_iban,
                                     to_iban=to_iban,
                                     transfer_concept=concept,
                                     transfer_type=transfer_type,
                                     transfer_date=transfer_date,
                                     transfer_amount=amount)

        try:
            with open(TRANSFERS_STORE_FILE, "r", encoding="utf-8", newline="") as file:
                transfer_list = json.load(file)
        except FileNotFoundError:
            transfer_list = []
        except json.JSONDecodeError as json_error:
            raise AccountManagementException("JSON Decode Error - Wrong JSON Format") from json_error

        for existe in transfer_list:
            if (existe["from_iban"] == new_tranfer.from_iban and
                    existe["to_iban"] == new_tranfer.to_iban and
                    existe["transfer_date"] == new_tranfer.transfer_date and
                    existe["transfer_amount"] == new_tranfer.transfer_amount and
                    existe["transfer_concept"] == new_tranfer.transfer_concept and
                    existe["transfer_type"] == new_tranfer.transfer_type):
                raise AccountManagementException("Duplicated transfer in transfer list")

        transfer_list.append(new_tranfer.to_json())

        try:
            with open(TRANSFERS_STORE_FILE, "w", encoding="utf-8", newline="") as file:
                json.dump(transfer_list, file, indent=2)
        except FileNotFoundError as file_error:
            raise AccountManagementException("Wrong file  or file path") from file_error
        except json.JSONDecodeError as json_error:
            raise AccountManagementException("JSON Decode Error - Wrong JSON Format") from json_error

        return new_tranfer.transfer_code


    def deposit_into_account(self, input_file:str)->str:
        """manages the deposits received for accounts"""
        try:
            with open(input_file, "r", encoding="utf-8", newline="") as file:
                i_d = json.load(file)
        except FileNotFoundError as ex:
            raise AccountManagementException("Error: file input not found") from ex
        except json.JSONDecodeError as ex:
            raise AccountManagementException("JSON Decode Error - Wrong JSON Format") from ex

        # comprobar valores del fichero
        try:
            deposit_iban = i_d["IBAN"]
            deposit_amount = i_d["AMOUNT"]
        except KeyError as e:
            raise AccountManagementException("Error - Invalid Key in JSON") from e


        deposit_iban = self.validate_iban(deposit_iban)
        myregex = re.compile(r"^EUR [0-9]{4}\.[0-9]{2}")
        res = myregex.fullmatch(deposit_amount)
        if not res:
            raise AccountManagementException("Error - Invalid deposit amount")

        d_a_f = float(deposit_amount[4:])
        if d_a_f == 0:
            raise AccountManagementException("Error - Deposit must be greater than 0")

        deposit_obj = AccountDeposit(to_iban=deposit_iban,
                                     deposit_amount=d_a_f)

        try:
            with open(DEPOSITS_STORE_FILE, "r", encoding="utf-8", newline="") as file:
                d_l = json.load(file)
        except FileNotFoundError as ex:
            d_l = []
        except json.JSONDecodeError as ex:
            raise AccountManagementException("JSON Decode Error - Wrong JSON Format") from ex

        d_l.append(deposit_obj.to_json())

        try:
            with open(DEPOSITS_STORE_FILE, "w", encoding="utf-8", newline="") as file:
                json.dump(d_l, file, indent=2)
        except FileNotFoundError as ex:
            raise AccountManagementException("Wrong file  or file path") from ex
        except json.JSONDecodeError as ex:
            raise AccountManagementException("JSON Decode Error - Wrong JSON Format") from ex

        return deposit_obj.deposit_signature


    def read_transactions_file(self):
        """loads the content of the transactions file
        and returns a list"""
        try:
            with open(TRANSACTIONS_STORE_FILE, "r", encoding="utf-8", newline="") as file:
                input_list = json.load(file)
        except FileNotFoundError as ex:
            raise AccountManagementException("Wrong file  or file path") from ex
        except json.JSONDecodeError as ex:
            raise AccountManagementException("JSON Decode Error - Wrong JSON Format") from ex
        return input_list


    def calculate_balance(self, iban:str)->bool:
        """calculate the balance for a given iban"""
        iban = self.validate_iban(iban)
        t_l = self.read_transactions_file()
        iban_found = False
        bal_s = 0
        for transaction in t_l:
            #print(transaction["IBAN"] + " - " + iban)
            if transaction["IBAN"] == iban:
                bal_s += float(transaction["amount"])
                iban_found = True
        if not iban_found:
            raise AccountManagementException("IBAN not found")

        last_balance = {"IBAN": iban,
                        "time": datetime.timestamp(datetime.now(timezone.utc)),
                        "BALANCE": bal_s}

        try:
            with open(BALANCES_STORE_FILE, "r", encoding="utf-8", newline="") as file:
                balance_list = json.load(file)
        except FileNotFoundError:
            balance_list = []
        except json.JSONDecodeError as ex:
            raise AccountManagementException("JSON Decode Error - Wrong JSON Format") from ex

        balance_list.append(last_balance)

        try:
            with open(BALANCES_STORE_FILE, "w", encoding="utf-8", newline="") as file:
                json.dump(balance_list, file, indent=2)
        except FileNotFoundError as ex:
            raise AccountManagementException("Wrong file  or file path") from ex
        return True
