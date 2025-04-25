"""Account manager module """
import json
from uc3m_money.account_management_exception import AccountManagementException
from uc3m_money.iban_balance import IbanBalance
from uc3m_money.transfer_request import TransferRequest
from uc3m_money.account_deposit import AccountDeposit
from uc3m_money.storage.transfers_json_store import TransfersJsonStore
from uc3m_money.storage.deposits_json_store import DepositsJsonStore
from uc3m_money.storage.balances_json_store import BalancesJsonStore


class AccountManager:
    """Clase AccountManager"""
    # pylint: disable = [invalid-name]
    class __AccountManager:

        #pylint: disable=too-many-arguments
        def create_transfer_request(self, from_iban: str,
                                    to_iban: str,
                                    concept: str,
                                    transfer_type: str,
                                    transfer_date: str,
                                    amount: float)->str:
            """first method: receives transfer info and
            stores it into a file"""
            new_transfer = TransferRequest(from_iban=from_iban,
                                         to_iban=to_iban,
                                         transfer_concept=concept,
                                         transfer_type=transfer_type,
                                         transfer_date=transfer_date,
                                         transfer_amount=amount)

            transfer_store = TransfersJsonStore()
            transfer_store.add_item(new_transfer)

            return new_transfer.transfer_code

        def deposit_into_account(self, input_file:str)->str:
            """manages the deposits received for accounts"""
            try:
                with open(input_file, "r", encoding="utf-8", newline="") as file:
                    datos_deposito = json.load(file)
            except FileNotFoundError as file_error:
                raise AccountManagementException("Error: file input not found") from file_error
            except json.JSONDecodeError as json_error:
                raise AccountManagementException("JSON Decode Error - Wrong JSON Format") \
                    from json_error

            # comprobar valores del fichero
            try:
                deposit_iban = datos_deposito["IBAN"]
                deposit_amount = datos_deposito["AMOUNT"]
            except KeyError as key_error:
                raise AccountManagementException("Error - Invalid Key in JSON") \
                    from key_error

            deposit = AccountDeposit(to_iban=deposit_iban,
                                         deposit_amount=deposit_amount)

            deposits_json_store = DepositsJsonStore()
            deposits_json_store.add_item(deposit)

            return deposit.deposit_signature


        def calculate_balance(self, iban:str)->bool:
            """calculate the balance for a given iban"""
            iban_balance = IbanBalance(iban)

            balance_store = BalancesJsonStore()
            balance_store.add_item(iban_balance)

            return True

    instance = None

    def __new__(cls):
        if not AccountManager.instance:
            AccountManager.instance = AccountManager.__AccountManager()
        return AccountManager.instance

    def __getattr__(self, item):
        return getattr(AccountManager.instance, item)

    def __setattr__(self, key, value):
        return setattr(AccountManager.instance, key, value)
