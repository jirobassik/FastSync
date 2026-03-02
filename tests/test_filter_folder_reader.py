from fast_sync.folder_reader.folder_filter_reader import FilterFolders


def test_filter_priority(filter_reader_fabric):
    reader = filter_reader_fabric()
    filter_args = reader._filters
    for filter_ in filter_args:
        assert hasattr(filter_, "priority")

        if isinstance(filter_, FilterFolders):
            assert filter_.priority == 0
        else:
            assert filter_.priority > 0


def test_first_el_is_filter_folders(filter_reader_fabric):
    reader = filter_reader_fabric()
    filter_args = reader._filters
    filter_ = filter_args[0]
    assert isinstance(filter_, FilterFolders)
