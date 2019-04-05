# -*- coding: utf-8 -*-

from blkswn._version import __version__
from blkswn._Stack import Stack
from blkswn._Queue import Queue
from blkswn._Fetcher import Singleton as Fetcher

__copyright__ = 'Copyright 2016 Walter Eaves'
__license__ = 'GPLv3'
__title__ = 'blkswn'

# appease flake8: the imports are purposeful
(__version__, Stack, Queue)
