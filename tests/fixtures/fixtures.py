from pathlib import Path

import pytest

from fast_sync.hash_content_folder.hash_content_folder_caching.cache_folder_creation import (
    CacheFolderCreation,
)
from fast_sync.utils.path_setup import PathSetup


@pytest.fixture(scope="session")
def path_setup():
    return PathSetup()


@pytest.fixture(scope="session")
def cache_folder_creation():
    def _cache_folder_creation(custom_path=None):
        return CacheFolderCreation(custom_path)

    return _cache_folder_creation


@pytest.fixture(scope="session")
def folder_structure_hash():
    return [
        (
            ("637a1e7b9756424ca2ad8309a7f50f0b", Path("json/t24.csv")),
            Path("/home/puzer/OS_emulate/TestEqual/json/t24.csv"),
        ),
        (
            ("738f7ca27b9cf853362f28fc16b8101f", Path("json/t1.json")),
            Path("/home/puzer/OS_emulate/TestEqual/json/t1.json"),
        ),
        (
            ("c6bc2e91406290bcf0000a1442cc4858", Path("json/t2.json")),
            Path("/home/puzer/OS_emulate/TestEqual/json/t2.json"),
        ),
        (
            ("637a1e7b9756424ca2ad8309a7f50f0b", Path("csv/t24.csv")),
            Path("/home/puzer/OS_emulate/TestEqual/csv/t24.csv"),
        ),
        (
            ("c6bc2e91406290bcf0000a1442cc4858", Path("csv/t2.json")),
            Path("/home/puzer/OS_emulate/TestEqual/csv/t2.json"),
        ),
        (
            ("637a1e7b9756424ca2ad8309a7f50f0b", Path("csv/t2.csv")),
            Path("/home/puzer/OS_emulate/TestEqual/csv/t2.csv"),
        ),
        (
            ("d600008f9526d19de7c55e2183ad6ad0", Path("pickle/t2.pickle")),
            Path("/home/puzer/OS_emulate/TestEqual/pickle/t2.pickle"),
        ),
        (
            ("8fa6d1b3de9969b2925c338d3a25554e", Path("pickle/t1.pickle")),
            Path("/home/puzer/OS_emulate/TestEqual/pickle/t1.pickle"),
        ),
    ]
