class User(object):

    def __new__(cls, counter):
        if not hasattr(cls, 'instance'):
                cls.instance = super(User, cls).__new__(cls, counter)
        return cls.instance

    def __init__(self, counter):
        self.conter = counter

    #def get_counter(self):
    #    return self.conter