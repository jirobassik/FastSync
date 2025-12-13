from collections import namedtuple

examples_cli = namedtuple('examples_cli', ['text', 'explaining'])

examples = (
    examples_cli(
        '1) python fast_sync.py -left "/home/folder/Music2" -right "/Smartphone/DCIM/Music3 missing left"',
        "View missing files in Music2"),
    examples_cli(
        '2) python fast_sync.py -left "/home/folder/Music2" -right "/Smartphone/DCIM/Music3 sync left"',
        'Sync files from Music3 to Music2'),
)
