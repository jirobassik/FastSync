import click

from fast_sync.cli.main import fast_sync_cli
from fast_sync.equal_resolver import EqualResolver


@fast_sync_cli.group(help="Work with dublicates files")
@click.option(
    "--folder",
    "-f",
    required=True,
    type=click.Path(exists=True, file_okay=False),
)
@click.decorators.pass_meta_key("equal_resolver")
def dublicates(equal_resolver: EqualResolver, folder):
    equal_resolver.path_setup(folder)


# noinspection PyUnresolvedReferences
@dublicates.command("resolve", help="View and choose to delete dublicates files")
@click.decorators.pass_meta_key("equal_resolver")
def resolve(equal_resolver: EqualResolver):
    equal_resolver.equal_resolver()
