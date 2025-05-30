"""Importaciones"""
from uc3m_money.storage.JSONStore import JsonStore
from uc3m_money.account_management_config import TRANSFERS_STORE_FILE
from uc3m_money.account_management_exception import AccountManagementException


class TransfersJsonStore:
    """Clase TransfersJsonStore"""
    # pylint: disable = [invalid-name]
    class __TransfersJsonStore(JsonStore):
        _file_name = TRANSFERS_STORE_FILE

        def add_item(self, item):
            for existe in self._data_list:
                if existe == item.to_json():
                    raise AccountManagementException("Duplicated transfer in transfer list")
            super().add_item(item)

    instance = None

    def __new__(cls):
        if not TransfersJsonStore.instance:
            TransfersJsonStore.instance = TransfersJsonStore.__TransfersJsonStore()
        return TransfersJsonStore.instance

    def __getattr__(self, item):
        return getattr(TransfersJsonStore, item)

    def __setattr__(self, key, value):
        return setattr(TransfersJsonStore, key, value)
