from .filters import FilterFolders, FilterExtensionsFolder


class FilterValues:
    __slots__ = ("_folders", "_extensions")

    def __init__(self, extensions=None, folders=None):
        if extensions is None:
            extensions = set()
        if folders is None:
            folders = set()
        self._extensions = set(extensions)
        self._folders = set(folders)

    def as_filters_values(self) -> tuple:
        return self._folders, self._extensions


class FilterContentManager(FilterValues):
    filters = [
        FilterFolders,
        FilterExtensionsFolder,
    ]

    def __init__(self, extensions=None, folders=None):
        super().__init__(extensions, folders)
        self.setup_filter_data()

    def setup_filter_data(self):
        filters_value_filters = zip(self.as_filters_values(), self.filters)
        for filter_data, filter_object in filters_value_filters:
            filter_object.filter_value = filter_data
