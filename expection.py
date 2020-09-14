class BaseError(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.code = kwargs.get('code', 400)
        self.msg = args[0] if len(args) > 0 else kwargs.get('data', '')
