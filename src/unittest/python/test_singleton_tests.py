"""Tests singleton"""
from unittest import TestCase

from uc3m_money import AccountManager
from uc3m_money.storage.balances_json_store import BalancesJsonStore
from uc3m_money.storage.deposits_json_store import DepositsJsonStore
from uc3m_money.storage.transfers_json_store import TransfersJsonStore

class TestSingleton(TestCase):
    """Clase para tests singleton"""
    def test_account_manager_singleton(self):
        """Funcion de test account manager singleton"""
        account_manager1 = AccountManager()
        account_manager2 = AccountManager()
        account_manager3 = AccountManager()
        self.assertEqual(account_manager1, account_manager2)
        self.assertEqual(account_manager2, account_manager3)
        self.assertEqual(account_manager1, account_manager3)

    def test_transfer_json_store_store(self):
        """Funcion de test transfer json store singleton"""
        transfer1 = TransfersJsonStore()
        transfer2 = TransfersJsonStore()
        transfer3 = TransfersJsonStore()
        self.assertEqual(transfer1, transfer2)
        self.assertEqual(transfer2, transfer3)
        self.assertEqual(transfer1, transfer3)

    def test_deposit_json_store(self):
        """Funcion de test deposit json store singleton"""
        deposit1 = DepositsJsonStore()
        deposit2 = DepositsJsonStore()
        deposit3 = DepositsJsonStore()
        self.assertEqual(deposit1, deposit2)
        self.assertEqual(deposit2, deposit3)
        self.assertEqual(deposit1, deposit3)

    def test_balances_json_store(self):
        """Funcion de test balances json store singleton"""
        balance1 = BalancesJsonStore()
        balance2 = BalancesJsonStore()
        balance3 = BalancesJsonStore()
        self.assertEqual(balance1, balance2)
        self.assertEqual(balance2, balance3)
        self.assertEqual(balance1, balance3)
