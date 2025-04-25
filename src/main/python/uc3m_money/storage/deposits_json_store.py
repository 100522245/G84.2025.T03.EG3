"""Importaciones"""
from uc3m_money.storage.JSONStore import JsonStore
from uc3m_money.account_management_config import DEPOSITS_STORE_FILE


class DepositsJsonStore:
    """Clase DepositsJsonStore"""
    # pylint: disable = [invalid-name]
    class __DepositsJsonStore(JsonStore):
        _file_name = DEPOSITS_STORE_FILE

    instance = None

    def __new__(cls):
        if not DepositsJsonStore.instance:
            DepositsJsonStore.instance = DepositsJsonStore.__DepositsJsonStore()
        return DepositsJsonStore.instance

    def __getattr__(self, item):
        return getattr(DepositsJsonStore.instance, item)

    def __setattr__(self, key, value):
        return setattr(DepositsJsonStore.instance, key, value)
