# tests/test_secure_storage.py
import json

import pytest
from typer.testing import CliRunner

from secure_storage import (
    DB_READ_ERROR,
    SUCCESS,
    __app_name__,
    __version__,
    cli,
    secure_storage,
)

runner = CliRunner()


def test_version():
    result = runner.invoke(cli.app, ["--version"])
    assert result.exit_code == 0
    assert f"{__app_name__} v{__version__}\n" in result.stdout


@pytest.fixture
def mock_json_file(tmp_path):
    todo = [{"Description": "Get some milk.", "Priority": 2, "Done": False}]
    db_file = tmp_path / "todo.json"
    with db_file.open("w") as db:
        json.dump(todo, db, indent=4)
    return db_file


test_data1 = {
    "filename": ["Clean", "the", "house"],
    "priority": 1,
    "todo": {
        "Description": "Clean the house.",
        "Priority": 1,
        "Done": False,
    },
}
test_data2 = {
    "filename": ["Wash the car"],
    "priority": 2,
    "todo": {
        "Description": "Wash the car.",
        "Priority": 2,
        "Done": False,
    },
}


@pytest.mark.parametrize(
    "filename, priority, expected",
    [
        pytest.param(
            test_data1["filename"],
            test_data1["priority"],
            (test_data1["todo"], SUCCESS),
        ),
        pytest.param(
            test_data2["filename"],
            test_data2["priority"],
            (test_data2["todo"], SUCCESS),
        ),
    ],
)
def test_add(mock_json_file, description, priority, expected):
    todoer = secure_storage.SecureStorage(mock_json_file)
    assert todoer.encrypt(description) == expected
    read = todoer._db_handler.read_secure_storage()
    assert len(read.encrypted_files) == 2
