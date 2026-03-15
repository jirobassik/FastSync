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
    ProgressBarFastSync,
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

    hash_content_folder_base = providers.Factory(HashContentFolder)
    hash_content_folder_caching_base = providers.Factory(
        HashContentFolderCaching,
    )

    hash_content_folder = providers.Factory(
        hash_content_folder_base,
        reader=readers.readers_selector,
    )

    hash_content_folder_caching = providers.Factory(
        hash_content_folder_caching_base,
        reader=readers.readers_selector,
        cache_path=cache.cache,
    )

    hashers_selector = providers.Selector(
        selector=hash_type,
        simple_hash=hash_content_folder,
        cache_hash=hash_content_folder_caching,
    )


class FastSyncContainer(containers.DeclarativeContainer):
    hashers = providers.DependenciesContainer()

    fast_sync_base = providers.Factory(FastSync)

    fast_sync_application = providers.Factory(
        fast_sync_base, hash_method=hashers.hashers_selector
    )


class Container(containers.DeclarativeContainer):
    reader_type = providers.Dependency(instance_of=str, default="simple_reader")
    hash_type = providers.Dependency(instance_of=str, default="simple_hash")

    reader = providers.Container(ReaderContainer, reader_type=reader_type)

    cache = providers.Container(CacheContainer)

    hasher_base = providers.Container(HashContainer)
    fast_sync_base = providers.Container(FastSyncContainer)

    # noinspection PyTypeChecker
    hasher = providers.Container(
        hasher_base, hash_type=hash_type, readers=reader, cache=cache
    )

    # noinspection PyTypeChecker
    fast_sync = providers.Container(fast_sync_base, hashers=hasher)


@containers.copy(HashContainer)
class ProgressBarHashContainer(HashContainer):
    hash_content_folder_base = providers.Factory(
        ProgressBarHashContentFolder,
    )
    hash_content_folder_caching_base = providers.Factory(
        ProgressBarHashContentFolderCaching,
    )


@containers.copy(FastSyncContainer)
class ProgressBarFastSyncContainer(FastSyncContainer):
    fast_sync_base = providers.Factory(ProgressBarFastSync)


@containers.copy(Container)
class ProgressBarContainer(Container):
    hasher_base = providers.Container(ProgressBarHashContainer)
    fast_sync_base = providers.Container(ProgressBarFastSyncContainer)
