class Point(dict):

    """Python Objects that act like Javascript Objects"""

    def __init__(self, *args, **kwargs):
        super(Point, self).__init__(*args, **kwargs)
        self.__dict__ = self
