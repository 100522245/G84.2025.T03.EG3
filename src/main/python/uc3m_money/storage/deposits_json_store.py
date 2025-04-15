from uc3m_money.storage.JSONStore import JsonStore
from uc3m_money.account_management_config import DEPOSITS_STORE_FILE

class DepositsJsonStore(JsonStore):
    _file_name = DEPOSITS_STORE_FILE