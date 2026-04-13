import click

from fast_sync.cli.main import CliApplicationsObj, fast_sync_cli
from fast_sync.cli.utils.decorators import path_setup_wrapper
from fast_sync.cli.utils.output_formaters.output_formater import OutputFormater


@fast_sync_cli.group(help="View missing files in chosen folder")
@path_setup_wrapper
@click.pass_obj
def missing(obj: CliApplicationsObj, left_folder, right_folder):
    obj.fast_sync.path_setup(left_folder, right_folder)
    obj.fast_sync.analyze()


# noinspection PyUnresolvedReferences
@missing.command("left", short_help="Missing files in left folder")
@click.decorators.pass_meta_key("output_formater")
@click.pass_obj
def view_left_missing(obj: CliApplicationsObj, output_formater: OutputFormater):
    output_formater(
        obj.fast_sync.left_missing_files(),
        missing_folder=obj.fast_sync.left_folder,
        reference_folder=obj.fast_sync.right_folder,
    )


# noinspection PyUnresolvedReferences
@missing.command("right", short_help="Missing files in right folder")
@click.decorators.pass_meta_key("output_formater")
@click.pass_obj
def view_right_missing(obj: CliApplicationsObj, output_formater: OutputFormater):
    output_formater(
        obj.fast_sync.right_missing_files(),
        missing_folder=obj.fast_sync.right_folder,
        reference_folder=obj.fast_sync.left_folder,
    )
