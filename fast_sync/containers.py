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


class CacheContainer(containers.DeclarativeContainer):
    cache = providers.Factory(CacheFolderCreation)


class HashContainer(containers.DeclarativeContainer):
    hash_type = providers.Dependency(instance_of=str, default="simple_hash")

    readers = providers.DependenciesContainer()
    cache = providers.DependenciesContainer()

    hash_content_folder = providers.Factory(
        HashContentFolder,
        reader=readers.readers_selector,
    )
    hash_content_folder_caching = providers.Factory(
        HashContentFolderCaching,
        reader=readers.readers_selector,
        cache_path=cache.cache,
    )

    hash_content_folder_progressbar = providers.Factory(
        ProgressBarHashContentFolder, **hash_content_folder.kwargs
    )
    hash_content_folder_caching_progressbar = providers.Factory(
        ProgressBarHashContentFolderCaching, **hash_content_folder_caching.kwargs
    )

    hashers_selector = providers.Selector(
        selector=hash_type,
        simple_hash=hash_content_folder,
        cache_hash=hash_content_folder_caching,
        simple_hash_progressbar=hash_content_folder_progressbar,
        cache_hash_progressbar=hash_content_folder_caching_progressbar,
    )


class FastSyncContainer(containers.DeclarativeContainer):
    hashers = providers.DependenciesContainer()

    fast_sync_application = providers.Factory(
        FastSync, hash_method=hashers.hashers_selector
    )


class Container(containers.DeclarativeContainer):
    reader_type = providers.Dependency(instance_of=str, default="simple_reader")
    hash_type = providers.Dependency(instance_of=str, default="simple_hash")

    reader = providers.Container(ReaderContainer, reader_type=reader_type)

    cache = providers.Container(CacheContainer)

    hasher = providers.Container(
        HashContainer, hash_type=hash_type, readers=reader, cache=cache
    )

    fast_sync = providers.Container(FastSyncContainer, hashers=hasher)
