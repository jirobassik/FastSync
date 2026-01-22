import pytest


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


@pytest.fixture(scope="session")
def filled_folder_factory(create_base_folder, fill_folder_content):
    def _create_filled_folder(name, structure):
        base_folder = create_base_folder(name)
        return fill_folder_content(base_folder, structure)

    return _create_filled_folder
