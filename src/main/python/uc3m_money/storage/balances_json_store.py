"""Importaciones"""
from uc3m_money.storage.JSONStore import JsonStore
from uc3m_money.account_management_config import BALANCES_STORE_FILE


class BalancesJsonStore:
    """Clase BalancesJsonStore"""
    # pylint: disable = [invalid-name]
    class __BalancesJsonStore(JsonStore):
        _file_name = BALANCES_STORE_FILE

    instance = None

    def __new__(cls):
        if not BalancesJsonStore.instance:
            BalancesJsonStore.instance = BalancesJsonStore.__BalancesJsonStore()
        return BalancesJsonStore.instance

    def __getattr__(self, item):
        return getattr(BalancesJsonStore, item)

    def __setattr__(self, key, value):
        return setattr(BalancesJsonStore, key, value)
