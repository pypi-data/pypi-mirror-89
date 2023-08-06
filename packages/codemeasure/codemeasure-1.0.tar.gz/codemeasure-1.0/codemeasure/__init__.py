# Author: DAVIDhaker
# At: 22 dec 2020
# Mail me: me@davidhaker.ru
from datetime import datetime


class Measure:
    def __init__(self, prefix: str = None):
        """
        :param prefix: Prefix for print the line with elapsed time.
        """
        self.prefix = prefix
        self.started_at = datetime.now()

    def __exit__(self, *args, **kwargs):
        print(
            (self.prefix + ': ' if self.prefix else '')
            + str(datetime.now() - self.started_at)
            + ' elapsed'
        )
