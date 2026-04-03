from dependency_injector import containers, providers

from fast_sync.duplicate_resolver.duplicate_resolver import EqualResolver


class EqualResolverContainer(containers.DeclarativeContainer):
    hashers = providers.DependenciesContainer()

    equal_resolver_application = providers.Factory(
        EqualResolver, hash_method=hashers.hashers_selector
    )
