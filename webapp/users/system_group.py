class SystemGroup(object):
    def __init__(self, **kwargs):
        for field in ('name', 'gid', 'members'):
            setattr(self, field, kwargs.get(field, None))
