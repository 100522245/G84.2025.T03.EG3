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
from uc3m_money.Attribute.Attribute import Attribute
from uc3m_money.Attribute.IBAN import IBAN
from uc3m_money.Attribute.Concept import Concept
from uc3m_money.Attribute.Transfer_amount import Transfer_amount
from uc3m_money.Attribute.Date import Date
from uc3m_money.Attribute.Transfer_type import Transfer_type
from uc3m_money.Attribute.Deposit_amount import Deposit_amount


class AccountManager:
    """Class for providing the methods for managing the orders"""
    def __init__(self):
        pass

    #pylint: disable=too-many-arguments
    def create_transfer_request(self, from_iban: str,
                                to_iban: str,
                                concept: str,
                                transfer_type: str,
                                transfer_date: str,
                                amount: float)->str:
        """first method: receives transfer info and
        stores it into a file"""
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
                datos_deposito = json.load(file)
        except FileNotFoundError as file_error:
            raise AccountManagementException("Error: file input not found") from file_error
        except json.JSONDecodeError as json_error:
            raise AccountManagementException("JSON Decode Error - Wrong JSON Format") from json_error

        # comprobar valores del fichero
        try:
            deposit_iban = datos_deposito["IBAN"]
            deposit_amount = datos_deposito["AMOUNT"]
        except KeyError as key_error:
            raise AccountManagementException("Error - Invalid Key in JSON") \
                from key_error

        deposit = AccountDeposit(to_iban=deposit_iban,
                                     deposit_amount=deposit_amount)

        try:
            with open(DEPOSITS_STORE_FILE, "r", encoding="utf-8", newline="") as file:
                deposit_list = json.load(file)
        except FileNotFoundError:
            deposit_list = []
        except json.JSONDecodeError as json_error:
            raise AccountManagementException("JSON Decode Error - Wrong JSON Format") from json_error

        deposit_list.append(deposit.to_json())

        try:
            with open(DEPOSITS_STORE_FILE, "w", encoding="utf-8", newline="") as file:
                json.dump(deposit_list, file, indent=2)
        except FileNotFoundError as file_error:
            raise AccountManagementException("Wrong file  or file path") from file_error
        except json.JSONDecodeError as json_error:
            raise AccountManagementException("JSON Decode Error - Wrong JSON Format") from json_error

        return deposit.deposit_signature


    def calculate_balance(self, iban:str)->bool:
        """calculate the balance for a given iban"""
        iban_balance = IBAN(iban)
        last_balance = iban_balance.to_json()

        try:
            with open(BALANCES_STORE_FILE, "r", encoding="utf-8", newline="") as file:
                balance_list = json.load(file)
        except FileNotFoundError:
            balance_list = []
        except json.JSONDecodeError as json_error:
            raise AccountManagementException("JSON Decode Error - Wrong JSON Format") from json_error

        balance_list.append(last_balance)

        try:
            with open(BALANCES_STORE_FILE, "w", encoding="utf-8", newline="") as file:
                json.dump(balance_list, file, indent=2)
        except FileNotFoundError as file_error:
            raise AccountManagementException("Wrong file  or file path") from file_error
        return True