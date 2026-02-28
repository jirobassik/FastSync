import click
from click import FileError
from loguru import logger

from fast_sync import (
    CacheFolderCreation,
    FolderReader,
)
from fast_sync.cli.utils.output_formaters.output_formater import OutputFormater
from fast_sync.folder_reader.folder_filter_reader import (
    FilterExtensionsFolder,
    FilterFolders,
)
from fast_sync.folder_reader.folder_filter_reader.folder_filter_reader import (
    FolderFilterReader,
)
from fast_sync.utils.error import (
    CacheFolderCreationError,
    NotValidFilterInput,
    OsPathResolverError,
)
from fast_sync.utils.progressbar import (
    ProgressBarFastSync,
    ProgressBarHashContentFolder,
    ProgressBarHashContentFolderCaching,
)

from .utils import CustomHelp, error_output
from .utils.custom_config_option import config_option
from .utils.error_output import PermissionDeniedError


@click.group(cls=CustomHelp)
@click.option("--hashing/--no-hashing", "-h/-Nh", default=False, help="Use hash for boost repeat calculations [Warning if the files "
                                                 "have the same name and different contents, "
                                                 "caching should not be used in this case]")
@click.option("--group/--no-group", "-g/-Ng", default=False, help="Group files by folders [Affects the output format]")
@click.option("--sort/--no-sort", "-s/-Ns", default=False, help="Sort files by name [Affects the output format]")
@click.option("--extensions", "-e", default=(), multiple=True, help="Filter files by extension")
@click.option("--folders", "-f", default=(), multiple=True, help="Exclude files based on folder")
@config_option(strict=True, roaming=False)
@click.pass_context
def fast_sync_cli(ctx, hashing, group, sort, extensions, folders):
    ctx.meta["output_formater"] = OutputFormater(grouped=group, sorted_=sort)

    click.echo("---" * 30)
    click.secho("Fast sync started", fg="green", bold=True)
    try:
        reader = FolderReader()
        if extensions or folders:
            reader = FolderFilterReader(
                FilterFolders(*folders),
                FilterExtensionsFolder(*extensions),
            )

        hash_method = ProgressBarHashContentFolder(reader)
        if hashing:
            cache_path = CacheFolderCreation()
            hash_method = ProgressBarHashContentFolderCaching(reader, cache_path)

        progress_bar_sync_manager = ProgressBarFastSync(hash_method)
    except NotValidFilterInput:
        logger.debug("Not valid filter input")
        error_output(
            "Not valid filter input", fix="view examples 'fast_sync.py --help'"
        )
    except CacheFolderCreationError as e:
        raise PermissionDeniedError(
            e.filename, hint="Try another folder with write and reade permissions"
        )
    except OsPathResolverError as e:
        raise FileError(e.filename, hint="Try another path")
    else:
        ctx.obj = progress_bar_sync_manager
    click.echo("---" * 30)
