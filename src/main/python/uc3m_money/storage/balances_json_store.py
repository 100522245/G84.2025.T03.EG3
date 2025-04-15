from uc3m_money.storage.JSONStore import JsonStore
from uc3m_money.account_management_config import BALANCES_STORE_FILE

class BalancesJsonStore(JsonStore):
    _file_name = BALANCES_STORE_FILE