import click

from cli.main import fast_sync_cli
from cli.utils.output_formaters.output_formater import meta_output_formater
from fast_sync.main import FastSync


@fast_sync_cli.group(help="View missing files in chosen folder")
def missing():
    pass


@missing.command('left', short_help="Missing files in left folder")
@click.pass_obj
def view_left_missing(obj: FastSync):
    meta_output_formater()(obj.left_missing_files(), missing_folder=obj.left_folder, reference_folder=obj.right_folder)


@missing.command('right', short_help="Missing files in right folder")
@click.pass_obj
def view_right_missing(obj: FastSync):
    meta_output_formater()(obj.right_missing_files(), missing_folder=obj.right_folder, reference_folder=obj.left_folder)
