import pwd


class SystemUser(object):
    def __init__(self):
        self.all_users = pwd.getpwall()
