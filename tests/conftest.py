from pathlib import Path

import pytest

from fast_sync import (
    CacheFolderCreation,
    FolderFilterReader,
    HashContentFolder,
    HashContentFolderCaching,
)
from fast_sync.containers.main_container import Container
from fast_sync.folder_reader.folder_filter_reader import (
    FilterExtensionsFolder,
    FilterFolders,
)
from fast_sync.main import FastSync
from tests.fixtures import *  # noqa: F403

FIXTURE_DIR_INTERNAL = Path(__file__).parent / "fixtures/test_folders"
FIXTURE_DIR_EXTERNAL = Path().home() / "OS_emulate"


class ConfigureFastSyncDefault:
    @staticmethod
    def configure_fast_sync_default(fast_sync_method: FastSync):
        return fast_sync_method

    @staticmethod
    def configure_filter_reader_default(folders: tuple = (), extensions: tuple = ()):
        return FolderFilterReader(
            FilterFolders(*folders),
            FilterExtensionsFolder(*extensions),
        )

    @staticmethod
    def configure_caching_fast_sync_default(path_to_cache):
        return FastSync(
            HashContentFolderCaching(
                cache_path=CacheFolderCreation(path_to_cache=path_to_cache)
            )
        )

    def configure_filter_reader_fast_sync_default(
        self, folders: tuple = (), extensions: tuple = ()
    ):
        reader = self.configure_filter_reader_default(folders, extensions)
        return FastSync(HashContentFolder(reader))


class ConfigureFastSyncDepInj:
    base_container = Container

    def configure_fast_sync_dep_inj(self, fast_sync_method: FastSync):
        return self.base_container().fast_sync.fast_sync_application

    def configure_filter_reader_fast_sync_dep_inj(
        self, folders: tuple = (), extensions: tuple = ()
    ):
        fast_sync_container = self.base_container(reader_type="filter_reader")
        fast_sync_container.reader.filter_extensions.set_args(*extensions)
        fast_sync_container.reader.filter_folder.set_args(*folders)
        return fast_sync_container.fast_sync.fast_sync_application()

    def configure_caching_fast_sync_dep_inj(self, path_to_cache):
        fast_sync_container = self.base_container(hash_type="cache_hash")
        fast_sync_container.cache(path_to_cache=path_to_cache)
        return fast_sync_container.fast_sync.fast_sync_application()

    def configure_filter_reader_dep_inj(
        self, folders: tuple = (), extensions: tuple = ()
    ):
        fast_sync_container = self.base_container()
        fast_sync_container.reader.filter_extensions.set_args(*extensions)
        fast_sync_container.reader.filter_folder.set_args(*folders)
        return fast_sync_container.reader.folder_readers.filter_reader()


configure_fast_sync_default_class = ConfigureFastSyncDefault()
configure_fast_sync_dep_inj_class = ConfigureFastSyncDepInj()


@pytest.fixture(
    scope="session",
    params=[
        configure_fast_sync_default_class.configure_fast_sync_default,
        configure_fast_sync_dep_inj_class.configure_fast_sync_dep_inj,
    ],
)
def default_fast_sync_fabric(request):
    def _default_fast_sync_fabric(left_folder, right_folder, fast_sync_method=FastSync):
        fast_sync = request.param(fast_sync_method)()
        fast_sync.path_setup(left_folder, right_folder)
        fast_sync.analyze()
        return fast_sync

    return _default_fast_sync_fabric


@pytest.fixture(
    scope="session",
    params=[
        configure_fast_sync_default_class.configure_caching_fast_sync_default,
        configure_fast_sync_dep_inj_class.configure_caching_fast_sync_dep_inj,
    ],
)
def caching_fast_sync_fabric(request):
    def _caching_fast_sync_fabric(left_folder, right_folder, path_to_cache):
        fast_sync = request.param(path_to_cache)
        fast_sync.path_setup(left_folder, right_folder)
        fast_sync.analyze()
        return fast_sync

    return _caching_fast_sync_fabric


@pytest.fixture(
    scope="session",
    params=[
        configure_fast_sync_default_class.configure_filter_reader_default,
        configure_fast_sync_dep_inj_class.configure_filter_reader_dep_inj,
    ],
)
def filter_reader_fabric(request):
    def _filter_reader_fabric(folders: tuple = (), extensions: tuple = ()):
        return request.param(folders, extensions)

    return _filter_reader_fabric


@pytest.fixture(
    scope="session",
    params=[
        configure_fast_sync_default_class.configure_filter_reader_fast_sync_default,
        configure_fast_sync_dep_inj_class.configure_filter_reader_fast_sync_dep_inj,
    ],
)
def filter_reader_fast_sync_fabric(request):
    def _filter_reader_fast_sync_fabric(
        left_folder,
        right_folder,
        folders: tuple,
        extensions: tuple,
    ):
        fast_sync = request.param(folders, extensions)
        fast_sync.path_setup(left_folder, right_folder)
        fast_sync.analyze()
        return fast_sync

    return _filter_reader_fast_sync_fabric


@pytest.fixture(scope="session")
def fast_sync_simple_folder_default_reader_left_empty(
    default_fast_sync_fabric,
    create_base_folder,
    right_folder_simple,
):
    return default_fast_sync_fabric(
        create_base_folder("left_folder"), right_folder_simple
    )


@pytest.fixture(scope="session")
def fast_sync_simple_folder_default_reader_right_empty(
    default_fast_sync_fabric,
    left_folder_simple,
    create_base_folder,
):
    return default_fast_sync_fabric(
        left_folder_simple, create_base_folder("right_folder")
    )


@pytest.fixture(scope="session")
def fast_sync_simple_folder_default_reader_all_empty(
    default_fast_sync_fabric,
    create_base_folder,
):
    return default_fast_sync_fabric(
        create_base_folder("left_folder"), create_base_folder("right_folder")
    )


@pytest.fixture(scope="session")
def fast_sync_simple_folder_default_reader(
    default_fast_sync_fabric,
    left_folder_simple,
    right_folder_simple,
):
    return default_fast_sync_fabric(left_folder_simple, right_folder_simple)


@pytest.fixture(scope="session")
def fast_sync_left_nested_simple_folder_default_reader(
    default_fast_sync_fabric,
    left_folder_nested_simple,
    right_folder_simple,
):
    return default_fast_sync_fabric(left_folder_nested_simple, right_folder_simple)


@pytest.fixture(scope="session")
def fast_sync_all_nested_simple_folder_default_reader(
    default_fast_sync_fabric,
    left_folder_nested_simple,
    right_folder_nested_simple,
):
    return default_fast_sync_fabric(
        left_folder_nested_simple, right_folder_nested_simple
    )


@pytest.fixture(scope="session")
def internal_folders_simple():
    def _internal_folders_simple(
        as_posix=False,
        left_f="Simple1",
        right_f="Simple2",
    ):
        left_folder = FIXTURE_DIR_INTERNAL / left_f
        right_folder = FIXTURE_DIR_INTERNAL / right_f
        return (
            (left_folder.as_posix(), right_folder.as_posix())
            if as_posix
            else (left_folder, right_folder)
        )

    return _internal_folders_simple
