from pathlib import Path
from typing import NamedTuple


class ExamplesCli(NamedTuple):
    text: str
    explaining: str


command_examples_fast_sync_cli = (
    ExamplesCli(
        f'fs --group --extensions ".mp3" missing -l "{Path("/home/user/Folder1").as_posix()}" -r "{Path("/home/user/Folder2").as_posix()}" left',
        "View missing files in Folder1 with group files and only `mp3` extensions.",
    ),
    ExamplesCli(
        f'fs --caching --extensions ".mp3" --folders "Folder3" sync -l "{Path("/home/user/Folder1").as_posix()}" -r "{Path("/home/user/Folder2").as_posix()}" right',
        "Sync files from Folder1 to Folder2 with caching (for boost repeat calculations). Only `mp3` extensions; exclude Folder3.",
    ),
    ExamplesCli(
        f"fs duplicates --folder {Path('/home/user/Folder1').as_posix()} resolve --view-delete",
        "Resolve duplicates files and view files that will be deleted.",
    ),
)
