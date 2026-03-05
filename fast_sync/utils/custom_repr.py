from reprlib import Repr

from fast_sync.utils.errors import HashContentFolderError, PathSetupError


class ReprLazyAttr(Repr):
    def __init__(self, error_except, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.error_except = error_except

    def repr_lazy_attr(self, obj, attr_name):
        try:
            attr_value = getattr(obj, attr_name)
        except self.error_except:
            attr_value = None
        return super().repr(attr_value)


hash_repr = ReprLazyAttr(HashContentFolderError, maxlist=1)
path_setup_repr = ReprLazyAttr(PathSetupError)
diff_folder_repr = Repr(maxdict=1)
path_repr = Repr(maxlong=1)
