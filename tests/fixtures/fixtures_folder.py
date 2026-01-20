import pytest


@pytest.fixture(scope="session")
def simple_folder_structure1():
    return {
        "folder1": {
            "file1.txt": "hello world",
            "data.json": '{"key": "value", "number": 123}',
            "config.yaml": "settings:\n  enabled: true",
            "folder2": {"data.json": '{"key": "value", "number": 123}'},
        }
    }


@pytest.fixture(scope="session")
def nested_simple_folder_structure1(simple_folder_structure1):
    return {
        "folder1": {
            "config.yaml": "settings:\n  enabled: true",
            "nested_folder1": simple_folder_structure1,
        }
    }


@pytest.fixture(scope="session")
def simple_folder_structure2():
    return {
        "folder1": {
            "file1.txt": "hello world",
            "file2.txt": "another content",
            "users.csv": "id,name,age\n1,Alice,30\n2,Bob,25",
        }
    }


@pytest.fixture(scope="session")
def create_base_folder(tmp_path_factory):
    def _create_base_folder(folder_name):
        return tmp_path_factory.mktemp(folder_name)

    return _create_base_folder


@pytest.fixture(scope="session")
def fill_folder_content():
    def _fill_folder_content(path_, folders):
        for key, value in folders.items():
            if isinstance(value, dict):
                new_path = path_ / key
                new_path.mkdir()
                _fill_folder_content(new_path, value)
            else:
                (path_ / key).write_text(value)
        return path_.as_posix()

    return _fill_folder_content
