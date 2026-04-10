from dependency_injector import containers, providers

from fast_sync.duplicate_resolver.duplicate_questions.main_question import (
    FilterDuplicateQuestion,
)
from fast_sync.duplicate_resolver.duplicate_resolver import DuplicateResolver


class DuplicateResolverContainer(containers.DeclarativeContainer):
    hashers = providers.DependenciesContainer()
    filter_method = providers.Factory(FilterDuplicateQuestion)

    duplicate_resolver_application = providers.Factory(
        DuplicateResolver,
        hashing_content=hashers.hashers_selector,
        filter_duplicates=filter_method,
    )
