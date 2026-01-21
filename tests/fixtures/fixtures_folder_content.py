import pytest


@pytest.fixture(scope="session")
def left_folder_simple_structure():
    return {
        "folder1": {
            "file1.txt": "hello world",
            "data.json": '{"key": "value", "number": 123}',
            "config.yaml": "settings:\n  enabled: true",
            "folder2": {"data.json": '{"key": "value", "number": 123}'},
        }
    }


@pytest.fixture(scope="session")
def left_folder_nested_simple_structure(left_folder_simple_structure):
    return {
        "folder1": {
            "config.yaml": "settings:\n  enabled: true",
            "nested_folder": left_folder_simple_structure,
        }
    }


@pytest.fixture(scope="session")
def right_folder_simple_structure():
    return {
        "folder1": {
            "file1.txt": "hello world",
            "file2.txt": "another content",
            "users.csv": "id,name,age\n1,Alice,30\n2,Bob,25",
        }
    }


@pytest.fixture(scope="session")
def right_folder_nested_simple_structure():
    return {
        "folder1": {
            "config.yaml": "settings:\n  enabled: true",
            "nested_folder": {
                "file2.txt": "another content",
                "users.csv": "id,name,age\n1,Alice,30\n2,Bob,25",
            },
        }
    }
