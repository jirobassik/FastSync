from .filters import FilterFolders, FilterExtensionsFolder


class FilterValues:
    __slots__ = ("_folders", "_extensions")

    def __init__(self, extensions=None, folders=None):
        self._extensions = extensions
        self._folders = folders

    @property
    def extensions(self):
        return self._extensions

    @property
    def folders(self):
        return self._folders


class FilterContentManager(FilterValues):
    filters = [
        FilterFolders,
        FilterExtensionsFolder,
    ]

    def __init__(self, extensions=None, folders=None):
        super().__init__(extensions, folders)
        self.setup_filter_data()

    def setup_filter_data(self):
        for filter_object in type(self).filters:
            filter_object.filter_value = getattr(self, filter_object.filter_name)
