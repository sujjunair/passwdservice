class SystemUser(object):
    def __init__(self, **kwargs):
        for field in ('name', 'uid', 'gid', 'comment', 'home', 'shell'):
            setattr(self, field, kwargs.get(field, None))
