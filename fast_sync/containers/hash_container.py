from dependency_injector import containers, providers

from fast_sync import (
    CacheFolderCreation,
    HashContentFolder,
    HashContentFolderCaching,
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
