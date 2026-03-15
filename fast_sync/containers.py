from dependency_injector import containers, providers

from fast_sync import (
    CacheFolderCreation,
    FastSync,
    FolderFilterReader,
    FolderReader,
    HashContentFolder,
    HashContentFolderCaching,
)
from fast_sync.folder_reader.folder_filter_reader import (
    FilterExtensionsFolder,
    FilterFolders,
)
from fast_sync.utils.progressbar import (
    ProgressBarHashContentFolder,
    ProgressBarHashContentFolderCaching,
)


class Container(containers.DeclarativeContainer):
    reader_type = providers.Dependency(instance_of=str, default="simple_reader")
    hash_type = providers.Dependency(instance_of=str, default="simple_hash")

    # Readers

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

    readers = providers.Selector(
        selector=reader_type,
        simple_reader=folder_readers.simple_reader,
        filter_reader=folder_readers.filter_reader,
    )

    # Cache

    cache = providers.Factory(CacheFolderCreation)

    # Hashes

    hash_content_folder = providers.Factory(
        HashContentFolder,
        reader=readers,
    )
    hash_content_folder_caching = providers.Factory(
        HashContentFolderCaching,
        reader=readers,
        cache_path=cache,
    )

    hash_content_folder_progressbar = providers.Factory(
        ProgressBarHashContentFolder, **hash_content_folder.kwargs
    )
    hash_content_folder_caching_progressbar = providers.Factory(
        ProgressBarHashContentFolderCaching, **hash_content_folder_caching.kwargs
    )

    hashers = providers.Selector(
        selector=hash_type,
        simple_hash=hash_content_folder,
        cache_hash=hash_content_folder_caching,
        simple_hash_progressbar=hash_content_folder_progressbar,
        cache_hash_progressbar=hash_content_folder_caching_progressbar,
    )

    # SyncManager

    fast_sync = providers.Factory(FastSync, hash_method=hashers)


class Container2(containers.DeclarativeContainer):
    reader_type = providers.Dependency(instance_of=str, default="simple_reader")
    hash_type = providers.Dependency(instance_of=str, default="simple_hash")

    # Readers

    folder_reader = providers.Factory(FolderReader)

    filter_folder = providers.Factory(FilterFolders)
    filter_extensions = providers.Factory(FilterExtensionsFolder)
    folder_filter_reader = providers.Factory(
        FolderFilterReader,
        filter_folder,
        filter_extensions,
    )
    readers = providers.Selector(
        selector=reader_type,
        simple_reader=folder_reader,
        filter_reader=folder_filter_reader,
    )

    # Hashes

    hash_content_folder = providers.Factory(
        HashContentFolder,
        reader=readers,
    )
    hash_content_folder_caching = providers.Factory(
        HashContentFolderCaching,
        reader=readers,
    )
    hashers = providers.Selector(
        selector=hash_type,
        simple_hash=hash_content_folder,
        cache_hash=hash_content_folder_caching,
    )

    # SyncManager

    fast_sync = providers.Factory(FastSync, hash_method=hashers)
