"""Importaciones"""
import json
from datetime import datetime, timezone
from uc3m_money.account_management_config import TRANSACTIONS_STORE_FILE
from uc3m_money.account_management_exception import AccountManagementException
from uc3m_money.data.Attribute.IBAN import IBAN


class IbanBalance:
    """Clase IbanBalance"""
    def __init__(self, iban_code):
        self._iban = IBAN(iban_code).value
        self.__last_balance_time = datetime.timestamp(datetime.now(
            timezone.utc))
        self.__balance = self.calculate_account_balance()

    def calculate_account_balance(self):
        """Metodo calculate_account_balance"""
        transactions_list = self.read_transactions_file()
        iban_found = False
        current_balance = 0
        for transaction in transactions_list:
            if transaction["IBAN"] == self._iban:
                current_balance += float(transaction["amount"])
                iban_found = True
        if not iban_found:
            raise AccountManagementException("IBAN not found")
        return current_balance

    def to_json(self):
        """Metodo to_json"""
        return {"IBAN": self._iban, "time": self.__last_balance_time,
                "BALANCE": self.__balance}

    def read_transactions_file(self):
        """Metodo read_transactions_file"""
        try:
            with open(TRANSACTIONS_STORE_FILE, "r", encoding="utf-8",
                      newline="") as file:
                input_list = json.load(file)
        except FileNotFoundError as file_error:
            raise AccountManagementException("Wrong file or file path") from file_error
        except json.JSONDecodeError as json_error:
            raise AccountManagementException("JSON Decode Error - Wrong JSON Format") \
                from json_error
        return input_list
