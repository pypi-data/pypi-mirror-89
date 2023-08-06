import inspect


class Command:
    def __init__(self, func, *, name: str = '', enabled: bool = True, help_doc: str = None):
        self.name = name or func.__name__
        if not isinstance(self.name, str):
            raise TypeError('Name of a command must be a string.')

        self.callback = func
        self.enabled = enabled

        if help_doc is not None:
            help_doc = inspect.cleandoc(help_doc)
        else:
            help_doc = inspect.getdoc(func)
            if isinstance(help_doc, bytes):
                help_doc = help_doc.decode('utf-8')

        self.help = help_doc
