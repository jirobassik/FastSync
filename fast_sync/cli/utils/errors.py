class ConfigFileCreationError(Exception):
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            super().__setattr__(key, value)
