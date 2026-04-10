import click

from fast_sync.cli.main import CliApplicationsObj, fast_sync_cli


@fast_sync_cli.group(help="Work with dublicates files")
@click.option(
    "--folder",
    "-f",
    required=True,
    type=click.Path(exists=True, file_okay=False),
)
@click.pass_obj
def duplicates(obj: CliApplicationsObj, folder):
    obj.duplicate_resolver.path_setup(folder)


# noinspection PyUnresolvedReferences
@duplicates.command("resolve", help="View and choose to delete dublicates files")
@click.pass_obj
def resolve(obj: CliApplicationsObj):
    obj.duplicate_resolver.resolve()
    click.secho("Duplicate files were successfully removed", fg="green")
