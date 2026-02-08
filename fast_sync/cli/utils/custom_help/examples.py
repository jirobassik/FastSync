from collections import namedtuple

examples_cli = namedtuple("examples_cli", ["text", "explaining"])

examples = (
    examples_cli(
        '1) uv run fast_sync.py -l "/home/puzer/OS_emulate/test_album_art1" -r "/home/puzer/OS_emulate/test_album_art2" missing left',
        "View missing files in test_album_art1",
    ),
    examples_cli(
        '2) uv run fast_sync.py -l "/home/puzer/OS_emulate/test_album_art1" -r "/home/puzer/OS_emulate/test_album_art2" -g -e ".mp3" missing left',
        "View missing files in test_album_art1 with group (-g) output and only mp3 extension (-e '.mp3')",
    ),
)
