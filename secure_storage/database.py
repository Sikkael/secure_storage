"""This module provides the RP To-Do database functionality."""
# secure_storage/database.py

import configparser
import json
from pathlib import Path
from typing import Any, Dict, List, NamedTuple

from secure_storage import DB_READ_ERROR, DB_WRITE_ERROR, JSON_ERROR, SUCCESS, ID_ERROR
from secure_storage.datasource import DataSource

DEFAULT_DB_FILE_PATH = Path.home().joinpath(
    "Data/" + "." + Path.home().stem + "_keystore.json"
)


def get_database_path(config_file: Path) -> Path:
    """Return the current path to the secure storage database."""
    config_parser = configparser.ConfigParser()
    config_parser.read(config_file)
    return Path(config_parser["General"]["database"])


def init_database(db_path: Path) -> int:
    """Create the Encrypted files' database."""
    try:
        db_path.parent.mkdir(parents=True, exist_ok=True)
        with db_path.open("w", encoding="utf-8") as fn:
            fn.write("[]")
        ef = Path(db_path.parent).joinpath("Encrypted Files")
        df = Path(db_path.parent).joinpath("Decrypted Files")
        ef.mkdir(parents=True, exist_ok=True)
        df.mkdir(parents=True, exist_ok=True)
        return SUCCESS
    except OSError:
        return DB_WRITE_ERROR


class DBResponse(NamedTuple):
    encrypted_files: Any
    error: int


class DatabaseHandler(DataSource):
    def __init__(self, db_path: Path) -> None:
        self._db_path = db_path

    def _read_secure_storage(self) -> DBResponse:
        try:
            with self._db_path.open("r") as db:
                try:
                    return DBResponse(json.load(db), SUCCESS)
                except json.JSONDecodeError:  # Catch wrong JSON format
                    return DBResponse([], JSON_ERROR)
        except OSError:  # Catch file IO problems
            return DBResponse([], DB_READ_ERROR)

    def _write_secure_storage(self, secure_storage_list: List[Dict[str, Any]]) -> DBResponse:
        try:
            with self._db_path.open("w") as db:
                json.dump(secure_storage_list, db, indent=4)
            return DBResponse(secure_storage_list, SUCCESS)
        except OSError:  # Catch file IO problems
            return DBResponse(secure_storage_list, DB_WRITE_ERROR)

    def add(self, obj) -> DBResponse:
        read = self._read_secure_storage()
        if read.error == DB_READ_ERROR:
            return DBResponse([], read.error)
        read.encrypted_files.append(obj)
        write = self._write_secure_storage(read.encrypted_files)
        if write.error == DB_WRITE_ERROR:
            return DBResponse([], write.error)
        return DBResponse([], write.error)

    def find(self, _id) -> DBResponse:
        """"""
        read = self._read_secure_storage()
        if read.error:
            return DBResponse([], read.error)
        try:
            enc_file = next(iter([file for file in read.encrypted_files if file['id'] == _id]))
            return DBResponse(enc_file, SUCCESS)
        except StopIteration:
            return DBResponse({}, ID_ERROR)

    def list(self) -> DBResponse:
        read = self._read_secure_storage()
        if read.error:
            return DBResponse([], read.error)
        return read

    def remove(self, _id: int) -> DBResponse:
        read = self.find(_id)
        if read.error == SUCCESS:
            enc_file_list = [fis for fis in self._read_secure_storage() if fis["id"] != _id]
            self._write_secure_storage(enc_file_list)
            return read
        return DBResponse({}, read.error)
