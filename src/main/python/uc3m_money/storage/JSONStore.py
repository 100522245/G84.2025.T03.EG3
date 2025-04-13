import json

from uc3m_money.account_management_exception import AccountManagementException


class JsonStore():
    _data_list = []
    _file_name = ""

    def __init__(self):
        self.load_list_from_file()

    def save_list_to_file(self):
        try:
            with (open(self._file_name, "w", encoding="utf-8", newline="")
                  as file):
                json.dump(self._data_list, file, indent=2)
        except FileNotFoundError as file_error:
            raise AccountManagementException("Wrong file or file path") from file_error

    def load_list_from_file(self):
        try:
            with (open(self._file_name, "r", encoding="utf-8", newline="") as
                  file):
                self._data_list = json.load(file)
        except FileNotFoundError:
            self._data_list = []
        except json.JSONDecodeError as json_error:
            raise AccountManagementException("JSON Decode Error - Wrong JSON Format") from json_error

    def add_item(self, item):
        self.load_list_from_file()
        self._data_list.append(item.to_json())
        self.save_list_to_file()