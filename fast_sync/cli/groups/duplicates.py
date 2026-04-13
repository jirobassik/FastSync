import click
import click_extra

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
@click.option(
    "--view-delete/--no-view-delete",
    "-v/-Nv",
    default=True,
    help="View files that will be deleted",
)
@click.pass_obj
def resolve(obj: CliApplicationsObj, view_delete: bool):
    # Called to invoke the method selection question
    files_to_delete = obj.duplicate_resolver.get_filters_duplicates

    if view_delete:
        click.secho("Files to delete:", fg="yellow", bold=True)
        for ind, file in enumerate(files_to_delete):
            click.echo(f"{ind + 1}. {file.relative_to(obj.duplicate_resolver.path)}")

    if click_extra.confirm(text="Delete files?", abort=True):
        obj.duplicate_resolver.resolve()
    click.secho("\nDuplicate files were successfully delete", fg="green")
