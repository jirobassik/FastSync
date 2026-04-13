from dependency_injector import containers, providers

from fast_sync.containers.hash_container import HashContainer
from fast_sync.containers.main_container import Container, FastSyncContainer
from fast_sync.utils.progressbar import (
    ProgressBarFastSync,
    ProgressBarHashContentFolder,
    ProgressBarHashContentFolderCaching,
)


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
