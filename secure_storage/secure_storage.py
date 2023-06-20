"""This module provides the RP To-Do model-controller."""
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, NamedTuple

from secure_storage import DB_READ_ERROR, ID_ERROR
from secure_storage.database import DatabaseHandler


class Filename(NamedTuple):
    todo: Dict[str, Any]
    error: int


class SecureStorage:
    def __init__(self, db_path: Path) -> None:
        self._db_handler = DatabaseHandler(db_path)

    def encrypt(self, filename: str) -> tuple:
        """Encrypt a new and store encryption key's and metadata to database."""
        encrypted_file = {
            "id": 0,
            'filename': filename,
            'datetime': datetime.now().strftime('%m/%d/%Y, %H:%M:%S'),
            'keyAES': "",
            'keyChaCha': "",
            "sha256": ""
        }
        write = self._db_handler.add(encrypted_file)
        return encrypted_file, write.error

    def decrypt(self, file_id: int) -> tuple:
        """Decrypt file."""
        file_infos, error = self._db_handler.find(file_id)
        return file_infos, error

    def get_secure_storage_list(self) -> tuple:
        """Return the current encrypted files list."""
        return self._db_handler.list()

    # def set_done(self, file_id: int) -> Filename:
    #     """Set a to-do as done."""
    #     read = self._db_handler.read_secure_storage()
    #     if read.error:
    #         return Filename({}, read.error)
    #     try:
    #         todo = read.encrypted_files_list[file_id - 1]
    #     except IndexError:
    #         return Filename({}, ID_ERROR)
    #     todo["Done"] = True
    #     write = self._db_handler.write_todos(read.encrypted_files_list)
    #     return Filename(todo, write.error)

    def remove(self, file_id: int) -> tuple:
        """Remove files."""

        file_infos, error = self._db_handler.remove(file_id)
        return file_infos, error

    # def remove_all(self) -> tuple:
    #     """Remove all to-dos from the database."""
    #     """write = self._db_handler._write_secure_storage([])"""
    #     return "",0
