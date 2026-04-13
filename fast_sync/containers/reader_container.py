from dependency_injector import containers, providers

from fast_sync import (
    FolderFilterReader,
    FolderReader,
)
from fast_sync.folder_reader.folder_filter_reader import (
    FilterExtensionsFolder,
    FilterFolders,
)


class ReaderContainer(containers.DeclarativeContainer):
    reader_type = providers.Dependency(instance_of=str, default="simple_reader")

    filter_folder = providers.Factory(FilterFolders)
    filter_extensions = providers.Factory(FilterExtensionsFolder)
    # noinspection PyTypeChecker
    folder_readers = providers.Aggregate(
        simple_reader=providers.Factory(FolderReader),
        filter_reader=providers.Factory(
            FolderFilterReader,
            filter_folder,
            filter_extensions,
        ),
    )

    readers_selector = providers.Selector(
        selector=reader_type,
        simple_reader=folder_readers.simple_reader,
        filter_reader=folder_readers.filter_reader,
    )
