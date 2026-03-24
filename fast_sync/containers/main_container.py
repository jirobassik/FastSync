from dependency_injector import containers, providers

from fast_sync import FastSync
from fast_sync.containers.equal_resolver_container import EqualResolverContainer
from fast_sync.containers.hash_container import CacheContainer, HashContainer
from fast_sync.containers.reader_container import ReaderContainer


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
    equal_resolver = providers.Container(EqualResolverContainer, hashers=hasher)
