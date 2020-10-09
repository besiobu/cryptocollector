class Persistor(object):
    """

    Base class for persistance objects.

    """
    
    def __init__(self):
        self.name = None

    def write(self, msg):
        pass